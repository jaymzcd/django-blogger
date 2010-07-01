from django.core.management.base import BaseCommand
import sys

from blogger.models import BloggerBlog

class Command(BaseCommand):
    help = 'Syncs existing Blogger blogs via their RSS feeds'

    def handle(self, *args, **options):
        count = 0
        for blog in BloggerBlog.objects.all():
            count += blog.sync_posts(forced=True)
            sys.stdout.write('Synced %s - %d posts\n' % (blog.name, count))
        sys.stdout.write('\nCOMPLETE: All blogs synced\n\n')

