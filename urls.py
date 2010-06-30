from django.conf.urls.defaults import patterns
from blogger.models import BloggerBlog

urlpatterns = patterns('',
    (r'^(?P<blog_id>\d+)/$', 'blogger.views.blog_via_pk', {}, 'blog_pk'),
    (r'^(?P<slug>[\w-]+)/$', 'blogger.views.blog_via_slug', {}, 'blog_slug'),
)



