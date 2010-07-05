from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template
from django.shortcuts import get_object_or_404
from blogger.models import BloggerBlog, BloggerPost

def blog(request, slug):
    blog = None
    _slug = slug # this always feels ugly

    try:
        blog = BloggerBlog.live.get(slug=_slug)
    except BloggerBlog.DoesNotExist:
        # ok, maybe try getting via the pk instead
        blog = get_object_or_404(BloggerBlog, pk=slug)

    # we have a blog otherwise we'd be at a 404
    _context = {'blog': blog}
    if blog.paginate:
        return object_list(request, blog.posts,
            paginate_by=blog.per_page,
            extra_context=_context
        )
    else:
        return object_list(request, blog.posts, extra_context=_context)

def post(request, post_id, post_title, blog_id=None, slug=None):
    # We don't actually need to know the blog, its just to structure the
    # url nicely along with the slugified text
    return object_detail(request, BloggerPost.live.all(), object_id=post_id)

def homepage(request):
    return direct_to_template(request, 'blogger/homepage.html')

def archive(request, year, month, slug=None, blog_id=None):
    return direct_to_template(request, 'blogger/homepage.html')