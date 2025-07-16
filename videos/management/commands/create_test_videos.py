"""
Management command to create test videos
"""
from django.core.management.base import BaseCommand
from videos.models import Video, Genre, VideoFile
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Create test videos for development'

    def handle(self, *args, **options):
        # Create genres
        action, created = Genre.objects.get_or_create(name='Action')
        if created:
            self.stdout.write(f'Created genre: {action.name}')
        
        comedy, created = Genre.objects.get_or_create(name='Comedy')
        if created:
            self.stdout.write(f'Created genre: {comedy.name}')
        
        drama, created = Genre.objects.get_or_create(name='Drama')
        if created:
            self.stdout.write(f'Created genre: {drama.name}')

        # Temporarily disable signal by monkey-patching
        from videos.signals import video_created_or_updated
        from django.db.models.signals import post_save
        from videos.models import Video as VideoModel
        
        post_save.disconnect(video_created_or_updated, sender=VideoModel)
        
        try:
            # Create videos
            video1, created = VideoModel.objects.get_or_create(
                title='Test Action Movie',
                defaults={
                    'description': 'An exciting action movie with lots of explosions and adventure.',
                    'genre': action,
                    'duration': timedelta(minutes=120)
                }
            )
            if created:
                self.stdout.write(f'Created video: {video1.title}')

            video2, created = VideoModel.objects.get_or_create(
                title='Test Comedy Show',
                defaults={
                    'description': 'A hilarious comedy that will make you laugh.',
                    'genre': comedy,
                    'duration': timedelta(minutes=90)
                }
            )
            if created:
                self.stdout.write(f'Created video: {video2.title}')

            video3, created = VideoModel.objects.get_or_create(
                title='Test Drama Series',
                defaults={
                    'description': 'A gripping drama series with compelling characters.',
                    'genre': drama,
                    'duration': timedelta(minutes=150)
                }
            )
            if created:
                self.stdout.write(f'Created video: {video3.title}')

            self.stdout.write(
                self.style.SUCCESS(f'Successfully created test data. Total videos: {VideoModel.objects.count()}')
            )
            
        finally:
            # Re-enable signal
            post_save.connect(video_created_or_updated, sender=VideoModel)
