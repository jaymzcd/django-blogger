from django.views.generic.list_detail import object_list
from django.shortcuts import get_object_or_404
from blogger.models import BloggerBlog

def blog_list(request, blog):
    if blog.paginate:
        return object_list(request, blog.posts,
            paginate_by=blog.per_page,
            extra_context={
                'blog': blog,
            }
        )
    else:
        return object_list(request, blog.posts,
            extra_context={
                'blog': blog,
            }
        )

def blog_via_slug(request, slug):
    _slug = slug # this always feels ugly
    blog = get_object_or_404(BloggerBlog, slug=_slug)
    return blog_list(request, blog)

def blog_via_pk(request, blog_id):
    blog = get_object_or_404(BloggerBlog, pk=blog_id)
    return blog_list(request, blog)


