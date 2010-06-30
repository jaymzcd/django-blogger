from django.views.generic.list_detail import object_list
from django.shortcuts import get_object_or_404
from blogger.models import BloggerBlog

def blog_via_slug(request, slug):
    _slug = slug # this always feels ugly
    blog = get_object_or_404(BloggerBlog, slug=_slug)
    return object_list(request, blog.posts)

def blog_via_pk(request, blog_id):
    blog = get_object_or_404(BloggerBlog, pk=blog_id)
    return object_list(request, blog.posts)

