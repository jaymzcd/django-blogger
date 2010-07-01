from django.contrib import admin
from blogger.models import BloggerBlog, BloggerUser, BloggerPost


class UserAdmin(admin.ModelAdmin):

    actions = ['create_blogs',]

    def create_blogs(self, request, queryset):
        for user in queryset:
            created = user.create_blogs()
        self.message_user(request, 'Created %d blogs' % created)
    create_blogs.short_description = 'Create the empty blogs from a particular user profile'

class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_posts', 'category', 'last_synced',)
    list_editable = ('category',)
    actions = ['sync_blog',]

    def sync_blog(self, request, queryset):
        for blog in queryset:
            blog.sync_posts(forced=True)
        self.message_user(request, 'Blogs now synced')
    sync_blog.short_description = 'Sync blogs regardless of last update time'


class PostAdmin(admin.ModelAdmin):
    list_display = ('blog', 'title', 'status', 'published',)
    list_filter = ('blog', 'published', 'status',)

admin.site.register(BloggerBlog, BlogAdmin)
admin.site.register(BloggerPost, PostAdmin)
admin.site.register(BloggerUser, UserAdmin)


