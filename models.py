from xml.dom.minidom import parse
import urllib
import re

from django.db import models
from django.template.defaultfilters import striptags, slugify
from datetime import datetime, timedelta

STATUS_CHOICES = (
    (0, 'Offline'),
    (5, 'Live'),
)

def get_links(xml):
    data = {}
    links = xml.getElementsByTagName('link')
    for link in links:
        data.update({link.getAttribute('rel'): link.getAttribute('href')})
    return data

class LiveManager(models.Manager):
    def get_query_set(self):
        return super(LiveManager, self).get_query_set().filter(status=5)

class BloggerUser(models.Model):

    # 'static' stuff
    _profile_url = 'http://www.blogger.com/feeds/%s/blogs'

    # ORM members
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, null=True, blank=True)
    blogger_id = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    def create_blogs(self):
        cnt = 0
        xml = parse(urllib.urlopen(BloggerUser._profile_url % self.blogger_id))
        for entry in xml.getElementsByTagName('entry'):
            blog_raw_id = entry.getElementsByTagName('id')[0].childNodes[0].data
            blog_name = entry.getElementsByTagName('title')[0].childNodes[0].data
            blog_url = None
            links = get_links(entry)
            blog = re.findall("([\d]+)", blog_raw_id)[-1] # grab last match
            django_blog, created = BloggerBlog.objects.get_or_create(
                blog_id=blog,
                name=blog_name,
                blogger_url=links['alternate'],
            )
            if created: cnt += 1
        return cnt


class BloggerBlog(models.Model):
    """
        Represents a blog on blogger via its id.
    """
    # 'static' stuff & choice fields
    _post_url = 'http://www.blogger.com/feeds/%s/posts/default'
    _teaser_length = 80
    HOUR_CHOICES = (
        (1, 1),
        (6, 6),
        (12, 12),
        (24, 24),
    )

    # our ORM members
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, null=True, blank=True) # see forms.py for info
    blog_id = models.CharField(max_length=100, unique=True)
    blogger_url = models.URLField(verify_exists=False)
    status = models.IntegerField(default=5, choices=STATUS_CHOICES) # switch it off from the main site
    banner = models.ImageField(upload_to='uploads/blogger/banners/', blank=True, null=True)
    banner.help_text = 'An image to use for the blogs header on the site'
    paginate = models.BooleanField(default=True)
    per_page = models.IntegerField(default=10)
    category = models.CharField(max_length=100, blank=True, null=True)
    category.help_text = 'For ordering the blogs under common categories'
    show_teaser = models.BooleanField(default=True)
    show_teaser.help_text = 'When enabled the full post will be stripped to a short text version'
    teaser_length = models.IntegerField(default=80)
    teaser_length.help_text = 'Tags will be stripped, so this is plain text words to show'
    order = models.IntegerField(default=5)
    order.help_text = 'Used to specifically order the blog list'
    last_synced = models.DateTimeField(blank=True, null=True)
    minimum_synctime = models.IntegerField(choices=HOUR_CHOICES, default=12)

    objects = models.Manager()
    live = LiveManager()

    class Meta:
        ordering = ('category', 'order', 'name')

    def __unicode__(self):
        return self.name

    @property
    def url(self):
        """ Returns the key part of the URL to access this blog via django """
        if self.slug:
            return self.slug
        else:
            return self.pk

    @models.permalink
    def get_absolute_url(self):
        return ('blogger:blog', [self.url])

    def sync_posts(self, forced=False):
        new_posts = 0
        if forced or self.needs_synced:
            _posts = list()
            xml = parse(urllib.urlopen(BloggerBlog._post_url % self.blog_id))
            entries = xml.getElementsByTagName('entry')
            for post in entries:
                post, created = BloggerPost.from_xml(post, self)
                if created: new_posts += 1
            self.last_synced = datetime.now()
            self.save()
            return new_posts
        else:
            return False

    @property
    def needs_synced(self):
        if self.last_synced+timedelta(hours=self.minimum_synctime) < datetime.now():
            return False
        return True

    @property
    def total_posts(self):
        return BloggerPost.objects.all().filter(blog=self).count()

    @property
    def posts(self):
        return BloggerPost.objects.all().filter(blog=self)

    @property
    def authors(self):
        return BloggerAuthor.objects.all().filter(blog=self)

class BloggerAuthor(models.Model):
    # This is for holding author info. This might seem the same as the user model
    # but its more for holding the basic author data that is present in the feed.
    # You can add more fields in here if you want to display something specific
    # for a blog post's author (eg. the photo field here)
    name = models.CharField(max_length=100)
    email = models.EmailField() # !unique, noreply@blogger.com can appear >1
    photo = models.ImageField(upload_to='uploads/blogger/authors/', blank=True, null=True)
    blog = models.ForeignKey(BloggerBlog)
    opensocial_id = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class BloggerPost(models.Model):
    # Holds post info as a form of caching/archiving and easy of use
    # When a request is made for blog posts it will create new entries
    # here for the blog.

    blog = models.ForeignKey(BloggerBlog)
    post_id = models.CharField(max_length=255, unique=True)
    published = models.DateTimeField()
    updated = models.DateTimeField()
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField()
    content_type = models.CharField(max_length=100, default='html')
    link_edit = models.URLField(verify_exists=False, blank=True, null=True)
    link_self = models.URLField(verify_exists=False, blank=True, null=True)
    link_alternate = models.URLField(verify_exists=False, blank=True, null=True)
    author = models.ForeignKey(BloggerAuthor, blank=True, null=True)
    status = models.IntegerField(default=5, choices=STATUS_CHOICES) # added to control on our end

    objects = models.Manager()
    live = LiveManager()

    def __unicode__(self):
        return '%s %s' % (self.title, self.blog.name)

    @staticmethod
    def from_xml(entry, _blog):
        """ Creates a new BloggerPost from input XML. See the below link for schema:
        http://code.google.com/apis/blogger/docs/2.0/developers_guide_protocol.html#RetrievingWithoutQuery
        The published & updated fields are converted to something mysql friendly
        """

        def get_content(tagname):
            try:
                return entry.getElementsByTagName(tagname)[0].childNodes[0].data
            except IndexError:
                return None

        author_xml = entry.getElementsByTagName('author')[0]
        try:
            osocial = author_xml.getElementsByTagName('gd:extendedProperty')[0].getAttribute('value'),
        except IndexError:
            osocial = 0

        _author, created = BloggerAuthor.objects.get_or_create(
            email=author_xml.getElementsByTagName('email')[0].childNodes[0].data,
            name=author_xml.getElementsByTagName('name')[0].childNodes[0].data,
            opensocial_id=osocial,
            blog=_blog,
        )

        links = get_links(entry)

        #TODO: this fails if content changes, refactor to pull out just the post_id
        # to do the lookup first. Then update fields with the data from the XML so
        # a resync causes updates

        created = False
        post_data = dict(
            blog=_blog,
            post_id=get_content('id'),
            published=get_content('published').replace('T', ' ')[:-6],
            updated=get_content('updated').replace('T', ' ')[:-6],
            title=get_content('title'),
            content=get_content('content'),
            content_type=entry.getElementsByTagName('content')[0].getAttribute('type'),
            author=_author,
            link_edit=links['edit'],
            link_self=links['self'],
            link_alternate=links['alternate'],
        )
        try:
            post = BloggerPost.objects.get(post_id=get_content('id'))
        except BloggerPost.DoesNotExist:
            created = True

        post = BloggerPost(**post_data)

        return [post, created]

    @property
    def wordcount(self):
        return len(striptags(self.content).split(' '))

    @property
    def remaining_words(self):
        count = self.wordcount - self.blog.teaser_length
        if count <= 0:
            return 0
        else:
            return count

    @property
    def teaser(self):
        return ' '.join(striptags(self.content).split(' ')[:self.blog.teaser_length])

    @property
    def list_content(self):
        if self.blog.show_teaser:
            return self.teaser
        else:
            return self.content

    @models.permalink
    def get_absolute_url(self):
        title = slugify(self.title)
        if self.blog.slug:
            return ('blogger:post', [self.blog.slug, self.pk, title])
        else:
            return ('blogger:post', [self.blog.pk, self.pk, title])

    class Meta:
        ordering = ('-published', '-updated')


