from django.conf.urls.defaults import patterns
from blogger.models import BloggerBlog

# When including this app within your own setup the blog url to use as a base should
# have 'blogger' for its namespace. Eg:
#
# (r'^blogs/', include('blogger.urls', namespace='blogger'))

urlpatterns = patterns('',
    (r'^(?P<blog_id>\d+)/$', 'blogger.views.blog_via_pk', {}, 'via_pk'),
    (r'^(?P<slug>[\w-]+)/$', 'blogger.views.blog_via_slug', {}, 'via_slug'),
)



