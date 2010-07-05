import re
from django import template
from django.db.models import Count
from blogger.models import BloggerBlog, BloggerPost

register = template.Library()

@register.inclusion_tag('blogger/tags/bloglist.html')
def bloglist():
    return {
        'blogs': BloggerBlog.live.all(),
    }

class PostContextNode(template.Node):
    def __init__(self, var_name):
        self.var_name = var_name

    def render(self, context):
        context[self.var_name] = BloggerPost.live.all()[:10]
        return ''

@register.tag('get_latest_posts')
def latest_posts(parser, token):
    """ returns context variable of blog posts """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        pass
    m = re.search(r'as (\w+)', arg)
    if not m:
        print "no parameters"
    var_name = m.groups()[0]
    return PostContextNode(var_name)

@register.inclusion_tag('blogger/tags/archive_counts.html')
def archive_counts(_blog=None):
    posts = BloggerPost.live.all()
    if _blog:
        posts = posts.filter(blog=_blog)

    counts = posts.extra(select={
        'year': "EXTRACT(year FROM published)",
        'month': "MONTHNAME(published)"
    }).values('year', 'month').annotate(count=Count('pk'))

    return {'counts': counts, 'blog': _blog}