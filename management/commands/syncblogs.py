from django.core.management.base import BaseCommand
import sys

from blogger.models import BloggerBlog

class Command(BaseCommand):
    help = 'Syncs existing Blogger blogs via their RSS feeds'

    def handle(self, *args, **options):
        total_count = 0
        for blog in BloggerBlog.objects.all():
            count = blog.sync_posts(forced=True)
            total_count += count
            sys.stdout.write('Synced %s - %d posts\n' % (blog.name, count))
        sys.stdout.write('\nCOMPLETE: All blogs synced - %d posts\n\n' % total_count)

