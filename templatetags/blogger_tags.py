from django import template
from blogger.models import BloggerBlog

register = template.Library()

@register.inclusion_tag('blogger/tags/bloglist.html')
def bloglist():
    return {
        'blogs': BloggerBlog.live.all(),
    }
