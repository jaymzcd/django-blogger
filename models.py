from xml.dom.minidom import parse
import urllib
import re

from django.db import models
from base.models import Nameable
from datetime import datetime, timedelta

class BloggerUser(Nameable):

    # 'static' stuff
    profile_url = 'http://www.blogger.com/feeds/%s/blogs'

    # ORM members
    blogger_id = models.CharField(max_length=100)

    def create_blogs(self):
        xml = parse(urllib.urlopen(BloggerUser.profile_url % self.blogger_id))
        for entry in xml.getElementsByTagName('entry'):
            blog_raw_id = entry.getElementsByTagName('id')[0].childNodes[0].data
            blog_name = entry.getElementsByTagName('title')[0].childNodes[0].data
            blog = re.findall("([\d]+)", blog_raw_id)[-1] # grab last match
            django_blog, created = BloggerBlog.objects.get_or_create(
                blog_id=blog,
                name=blog_name,
            )


class BloggerBlog(Nameable):
    """
        Represents a blog on blogger via its id.
    """
    # 'static' stuff & choice fields
    post_url = 'http://www.blogger.com/feeds/%s/posts/default'
    HOUR_CHOICES = (
        (1, 1),
        (6, 6),
        (12, 12),
        (24, 24),
    )

    # our ORM members
    blog_id = models.CharField(max_length=100, unique=True)
    last_synced = models.DateTimeField(blank=True, null=True)
    minimum_synctime = models.IntegerField(choices=HOUR_CHOICES, default=12)

    def sync_posts(self, forced=False):
        if forced or self.needs_synced:
            _posts = list()
            xml = parse(urllib.urlopen(BloggerBlog.post_url % self.blog_id))
            entries = xml.getElementsByTagName('entry')
            for post in entries:
                BloggerPost.from_xml(post, self)
            self.last_synced = datetime.now()
            self.save()
            return True
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


class PostManager(models.Manager):
    def get_query_set(self):
        return super(PostManager, self).get_query_set().filter(status=5)

class BloggerPost(models.Model):
    # Holds post info as a form of caching/archiving and easy of use
    # When a request is made for blog posts it will create new entries
    # here for the blog.

    STATUS_CHOICES = (
        (0, 'Offline'),
        (5, 'Live'),
    )

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
    author_name = models.CharField(max_length=200)
    author_email = models.EmailField(blank=True, null=True)

    status = models.IntegerField(default=5, choices=STATUS_CHOICES) # added to control on our end

    live = PostManager()
    objects = models.Manager()

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

        post, created = BloggerPost.objects.get_or_create(
            blog=_blog,
            post_id=get_content('id'),
            published=get_content('published').replace('T', ' ')[:-6],
            updated=get_content('updated').replace('T', ' ')[:-6],
            title=get_content('title'),
            content=get_content('content'),
            content_type=entry.getElementsByTagName('content')[0].getAttribute('type'),
        )
        return [post, created]

    class Meta:
        ordering = ('-published', '-updated')
