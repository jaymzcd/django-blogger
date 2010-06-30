from django.views.generic.list_detail import object_list
from blogger.models import BloggerBlog, BloggerPost

def blog(request, slug):

    return object_list(request, BloggerPost.objects.all())