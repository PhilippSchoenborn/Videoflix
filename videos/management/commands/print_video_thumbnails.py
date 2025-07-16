from django.core.management.base import BaseCommand
from videos.models import Video

class Command(BaseCommand):
    help = 'Prints all videos and their thumbnail URLs for debugging.'

    def handle(self, *args, **options):
        videos = Video.objects.all()
        for v in videos:
            self.stdout.write(f"ID: {v.id} | Title: {v.title} | Thumbnail: {v.thumbnail} | get_thumbnail_url: {v.get_thumbnail_url}")
