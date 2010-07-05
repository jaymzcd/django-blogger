from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template
from django.shortcuts import get_object_or_404
from blogger.models import BloggerBlog, BloggerPost

# All the blog views depend on having a blog variable set to filter out on the
# archive counts. Rather than mess with adding a context processor for the whole
# site keep it here
_context = {'blog': None}

def blog(request, slug):
    _blog = None
    _slug = slug # this always feels ugly

    try:
        _blog = BloggerBlog.live.get(slug=_slug)
    except BloggerBlog.DoesNotExist:
        # ok, maybe try getting via the pk instead
        _blog = get_object_or_404(BloggerBlog, pk=slug)

    # we have a _blog otherwise we'd be at a 404 now
    _context.update({'blog': _blog})
    if _blog.paginate:
        return object_list(request, _blog.posts,
            paginate_by=_blog.per_page,
            extra_context=_context
        )
    else:
        return object_list(request, _blog.posts, extra_context=_context)

def post(request, post_id, post_title, slug):
    # We don't actually need to know the blog, its just to structure the
    # url nicely along with the slugified text. (the slug arg)
    return object_detail(request, BloggerPost.live.all(), object_id=post_id,
        extra_context=_context)

def homepage(request):
    _context.update({'blog': None})
    return direct_to_template(request, 'blogger/homepage.html',
        extra_context=_context)

def archive(request, year, month, slug=None, blog_id=None):
    return direct_to_template(request, 'blogger/homepage.html',
        extra_context=_context)