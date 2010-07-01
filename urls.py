from django.conf.urls.defaults import patterns
from blogger.models import BloggerBlog

# When including this app within your own setup the blog url to use as a base should
# have 'blogger' for its namespace. Eg:
#
# (r'^blogs/', include('blogger.urls', namespace='blogger'))

urlpatterns = patterns('blogger.views',
    # These feel like I'm not being completely DRY, moist perhaps...
    (r'^(?P<blog_id>\d+)/(?P<post_id>\d+)/(?P<post_title>[\w-]+)/$', 'post', {}, 'post_via_pk'),
    (r'^(?P<slug>[\w-]+)/(?P<post_id>\d+)/(?P<post_title>[\w-]+)/$', 'post', {}, 'post_via_slug'),

    (r'^(?P<blog_id>\d+)/$', 'blog', {}, 'via_pk'),
    (r'^(?P<slug>[\w-]+)/$', 'blog', {}, 'via_slug'),

    (r'^$', 'homepage', {}, 'home'),
)
