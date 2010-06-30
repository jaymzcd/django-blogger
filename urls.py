from django.conf.urls.defaults import patterns
from blogger.models import BloggerBlog

urlpatterns = patterns('',
    (r'^(?P<slug>[\w-]+)/$', 'blogger.views.blog', {}, 'blog'),
)



