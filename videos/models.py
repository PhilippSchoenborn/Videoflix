"""
Video models for Videoflix application
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

User = get_user_model()


class Genre(models.Model):
    """
    Genre model for categorizing videos
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text=_('Genre name (e.g., Action, Comedy, Drama)')
    )
    description = models.TextField(
        blank=True,
        help_text=_('Optional description of the genre')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')
    
    def __str__(self):
        return self.name


class Video(models.Model):
    @property
    def get_thumbnail_url(self):
        """
        Liefert die URL zum Thumbnail-Bild oder einen Platzhalter, falls nicht vorhanden.
        """
        if self.thumbnail and hasattr(self.thumbnail, 'url') and self.thumbnail.url:
            return self.thumbnail.url
        if self.thumbnail_url:
            return self.thumbnail_url
        return '/static/images/video-placeholder.png'
    """
    Main video model
    """
    QUALITY_CHOICES = [
        ('120p', '120p'),
        ('360p', '360p'),
        ('720p', '720p'),
        ('1080p', '1080p'),
    ]
    
    AGE_RATING_CHOICES = [
        ('FSK 0', 'FSK 0'),
        ('FSK 6', 'FSK 6'),
        ('FSK 12', 'FSK 12'),
        ('FSK 16', 'FSK 16'),
        ('FSK 18', 'FSK 18'),
    ]
    
    title = models.CharField(
        max_length=200,
        help_text=_('Video title')
    )
    description = models.TextField(
        help_text=_('Video description')
    )
    thumbnail = models.ImageField(
        upload_to='video_thumbnails/',
        blank=True,
        null=True,
        help_text=_('Video thumbnail image')
    )
    thumbnail_url = models.URLField(
        blank=True,
        null=True,
        help_text=_('External thumbnail URL (used if no image file uploaded)')
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='videos',
        help_text=_('Video genre')
    )
    duration = models.DurationField(
        help_text=_('Video duration'),
        null=True,
        blank=True
    )
    age_rating = models.CharField(
        max_length=10,
        choices=AGE_RATING_CHOICES,
        default='FSK 16',
        help_text=_('Age rating classification')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(
        default=False,
        help_text=_('Whether this video should be featured on homepage')
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Video')
        verbose_name_plural = _('Videos')
    
    def __str__(self):
        return self.title
    
    def get_default_quality(self):
        """
        Get the highest available quality for this video
        """
        qualities = self.video_files.values_list('quality', flat=True)
        for quality in ['1080p', '720p', '360p', '120p']:
            if quality in qualities:
                return quality
        return None
    
    # Kein automatischer process_video_upload-Aufruf mehr hier – das übernimmt das Signal beim VideoFile




class VideoFile(models.Model):
    """
    Model to store different quality versions of videos
    """
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        related_name='video_files'
    )
    quality = models.CharField(
        max_length=10,
        choices=Video.QUALITY_CHOICES,
        help_text=_('Video quality')
    )
    file = models.FileField(
        upload_to='videos/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'webm', 'avi'])],
        help_text=_('Video file')
    )
    file_size = models.BigIntegerField(
        help_text=_('File size in bytes')
    )
    is_processed = models.BooleanField(
        default=False,
        help_text=_('Whether the video has been processed')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['video', 'quality']
        verbose_name = _('Video File')
        verbose_name_plural = _('Video Files')
    


    def __str__(self):
        return f"{self.video.title} - {self.quality}"



# Signal-Handler am Ende der Datei
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=VideoFile)
def video_file_post_save(sender, instance, created, **kwargs):
    # Nur beim ersten unverarbeiteten Upload process_video_upload asynchron starten
    if created and not instance.is_processed:
        from .utils import process_video_upload
        from django_rq import get_queue
        queue = get_queue('default')
        queue.enqueue(process_video_upload, instance.video.id)


class WatchProgress(models.Model):
    """
    Model to track user's watch progress
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='watch_progress'
    )
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        related_name='watch_progress'
    )
    progress_seconds = models.PositiveIntegerField(
        default=0,
        help_text=_('Progress in seconds')
    )
    last_resolution = models.CharField(
        max_length=10,
        default='720p',
        choices=[
            ('120p', '120p'),
            ('360p', '360p'),
            ('480p', '480p'),
            ('720p', '720p'),
            ('1080p', '1080p'),
        ],
        help_text=_('Last used video resolution')
    )
    last_watched = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(
        default=False,
        help_text=_('Whether the video has been completed')
    )
    
    class Meta:
        unique_together = ['user', 'video']
        verbose_name = _('Watch Progress')
        verbose_name_plural = _('Watch Progress')
    
    def __str__(self):
        return f"{self.user.username} - {self.video.title}"
    
    def get_progress_percentage(self):
        """
        Calculate progress percentage
        """
        if self.video.duration:
            total_seconds = self.video.duration.total_seconds()
            if total_seconds > 0:
                return min(100, (self.progress_seconds / total_seconds) * 100)
        return 0
