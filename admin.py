from django.contrib import admin
from blogger.models import BloggerBlog, BloggerUser, BloggerPost

def sync_blog(modeladmin, request, queryset):
    for blog in queryset:
        blog.sync_posts(forced=True)
sync_blog.short_description = 'Sync blogs regardless of last update time'

def create_blogs(modeladmin, request, queryset):
    for user in queryset:
        user.create_blogs()
create_blogs.short_description = 'Create the empty blogs from a particular user profile'

class UserAdmin(admin.ModelAdmin):
    actions = [create_blogs,]

class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_posts', 'last_synced',)
    actions = [sync_blog,]

class PostAdmin(admin.ModelAdmin):
    list_display = ('blog', 'title', 'status', 'published',)
    list_filter = ('blog', 'published', 'status',)

admin.site.register(BloggerBlog, BlogAdmin)
admin.site.register(BloggerPost, PostAdmin)
admin.site.register(BloggerUser, UserAdmin)


