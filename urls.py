from django.conf.urls.defaults import patterns
from blogger.models import BloggerBlog

# When including this app within your own setup the blog url to use as a base should
# have 'blogger' for its namespace. Eg:
#
# (r'^blogs/', include('blogger.urls', namespace='blogger'))

urlpatterns = patterns('',
    (r'^(?P<blog_id>\d+)/(?P<post_id>\d+)/(?P<post_title>[\w-]+)/$', 'blogger.views.post', {}, 'post_via_pk'),
    (r'^(?P<slug>[\w-]+)/(?P<post_id>\d+)/(?P<post_title>[\w-]+)/$', 'blogger.views.post', {}, 'post_via_slug'),


    (r'^(?P<blog_id>\d+)/$', 'blogger.views.blog', {}, 'via_pk'),
    (r'^(?P<slug>[\w-]+)/$', 'blogger.views.blog', {}, 'via_slug'),

)



