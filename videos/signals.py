"""
Django signals for videos app
"""
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from django.conf import settings
from django_rq import get_queue
from .models import Video, VideoFile, WatchProgress, Genre
from .utils import process_video_upload, get_video_duration
import logging
import os

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Video)
def video_created_or_updated(sender, instance, created, **kwargs):
    """
    Signal triggered when a video is created or updated
    """
    if created:
        logger.info(f'New video created: {instance.title} (ID: {instance.id})')
        
        # Set initial processing status if the field exists
        if hasattr(instance, 'is_processed'):
            instance.is_processed = False
            instance.save(update_fields=['is_processed'])
        
        # Trigger background processing if video file exists
        if hasattr(instance, 'video_file') and instance.video_file:
            try:
                # Queue video processing job
                queue = get_queue('default')
                job = queue.enqueue(
                    process_video_upload,
                    instance.id,
                    timeout='30m'  # 30 minutes timeout for video processing
                )
                logger.info(f'Video processing job queued for video {instance.id}: {job.id}')
                
            except Exception as e:
                logger.error(f'Error queuing video processing for video {instance.id}: {str(e)}')
    
    else:
        logger.info(f'Video updated: {instance.title} (ID: {instance.id})')


@receiver(post_save, sender=VideoFile)
def video_file_created(sender, instance, created, **kwargs):
    """
    Signal triggered when a video file is created
    """
    if created:
        logger.info(f'New video file created: {instance.quality} quality for video {instance.video.title}')
        
        # Calculate file size if not set
        if not instance.file_size and instance.file:
            try:
                instance.file_size = instance.file.size
                instance.save(update_fields=['file_size'])
                logger.info(f'File size calculated for video file {instance.id}: {instance.file_size} bytes')
            except Exception as e:
                logger.error(f'Error calculating file size for video file {instance.id}: {str(e)}')


@receiver(post_save, sender=WatchProgress)
def watch_progress_updated(sender, instance, created, **kwargs):
    """
    Signal triggered when watch progress is created or updated
    """
    if created:
        logger.info(f'Watch progress started: User {instance.user.email} started watching {instance.video.title}')
    else:
        # Check if video was completed
        if instance.video.duration and instance.video.duration.total_seconds() > 0:
            progress_percentage = (instance.progress_seconds / instance.video.duration.total_seconds()) * 100
            
            if progress_percentage >= 90 and not getattr(instance, '_completion_logged', False):
                logger.info(f'Video completed: User {instance.user.email} completed {instance.video.title}')
                instance._completion_logged = True
                
            elif progress_percentage >= 50 and not getattr(instance, '_halfway_logged', False):
                logger.info(f'Video halfway: User {instance.user.email} reached 50% of {instance.video.title}')
                instance._halfway_logged = True


@receiver(post_save, sender=Genre)
def genre_created_or_updated(sender, instance, created, **kwargs):
    """
    Signal triggered when a genre is created or updated
    """
    if created:
        logger.info(f'New genre created: {instance.name}')
    else:
        logger.info(f'Genre updated: {instance.name}')


@receiver(pre_delete, sender=Video)
def video_deletion_cleanup(sender, instance, **kwargs):
    """
    Signal triggered before video deletion
    Clean up related files and data
    """
    logger.warning(f'Video deletion initiated: {instance.title} (ID: {instance.id})')
    
    # Clean up video files from storage
    try:
        if instance.video_file and os.path.exists(instance.video_file.path):
            os.remove(instance.video_file.path)
            logger.info(f'Main video file deleted: {instance.video_file.path}')
            
        if instance.thumbnail and os.path.exists(instance.thumbnail.path):
            os.remove(instance.thumbnail.path)
            logger.info(f'Thumbnail deleted: {instance.thumbnail.path}')
            
    except Exception as e:
        logger.error(f'Error cleaning up files for video {instance.id}: {str(e)}')


@receiver(post_delete, sender=Video)
def video_deleted(sender, instance, **kwargs):
    """
    Signal triggered after video deletion
    """
    logger.info(f'Video deleted: {instance.title} (ID: {instance.id})')


@receiver(pre_delete, sender=VideoFile)
def video_file_deletion_cleanup(sender, instance, **kwargs):
    """
    Signal triggered before video file deletion
    Clean up the actual file from storage
    """
    logger.info(f'Video file deletion initiated: {instance.quality} quality for video {instance.video.title}')
    
    try:
        if instance.file and os.path.exists(instance.file.path):
            os.remove(instance.file.path)
            logger.info(f'Video file deleted from storage: {instance.file.path}')
    except Exception as e:
        logger.error(f'Error deleting video file {instance.id}: {str(e)}')


@receiver(post_delete, sender=VideoFile)
def video_file_deleted(sender, instance, **kwargs):
    """
    Signal triggered after video file deletion
    """
    logger.info(f'Video file deleted: {instance.quality} quality for video {instance.video.title}')
