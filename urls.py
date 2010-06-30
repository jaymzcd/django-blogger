from django.conf.urls.defaults import patterns
from blogger.models import BloggerBlog

urlpatterns = patterns('',
    (r'^(?P<slug>[\w-]+)$', 'django.views.generic.list_detail.object_list', {
            'queryset': BloggerBlog.objects.all(),
        }, 'blog'),
)
