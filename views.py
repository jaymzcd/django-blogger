from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template
from django.shortcuts import get_object_or_404
from blogger.models import BloggerBlog, BloggerPost


def blog(request, slug=None, blog_id=None):
    blog = None
    if slug:
        _slug = slug # this always feels ugly
        blog = get_object_or_404(BloggerBlog, slug=_slug)
    if blog_id:
        blog = get_object_or_404(BloggerBlog, pk=blog_id)

    # we have a blog otherwise we'd be at a 404
    _context = {'blog': blog}
    if blog.paginate:
        return object_list(request, blog.posts,
            paginate_by=blog.per_page,
            extra_context=_context
        )
    else:
        return object_list(request, blog.posts,
            extra_context={
                'blog': _context,
            }
        )

def post(request, post_id, post_title, blog_id=None, slug=None):
    # We don't actually need to know the blog, its just to structure the
    # url nicely along with the slugified text
    return object_detail(request, BloggerPost.live.all(), object_id=post_id)

def homepage(request):
    return direct_to_template(request, 'blogger/homepage.html')

def archive(request, year, month):
    return direct_to_template(request, 'blogger/homepage.html')