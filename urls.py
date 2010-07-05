from django.conf.urls.defaults import patterns
from blogger.models import BloggerBlog

# When including this app within your own setup the blog url to use as a base should
# have 'blogger' for its namespace. Eg:
#
# (r'^blogs/', include('blogger.urls', namespace='blogger'))

urlpatterns = patterns('blogger.views',
    # These feel like I'm not being completely DRY, moist perhaps...

    # Archive links
    (r'^(?P<slug>[\w-]+)/(?P<year>\d{4})/(?P<month>\w+)/$', 'archive', {}, 'archive'),
    (r'^(?P<year>\d{4})/(?P<month>\w+)/$', 'archive', {}, 'archive'),

    # Permalinks for blogs
    (r'^(?P<slug>[\w-]+)/(?P<post_id>\d+)/(?P<post_title>[\w-]+)/$', 'post', {}, 'post'),

    # Blog landing pages
    (r'^(?P<slug>[\w-]+)/$', 'blog', {}, 'blog'),

    # Index
    (r'^$', 'homepage', {}, 'home'),
)
