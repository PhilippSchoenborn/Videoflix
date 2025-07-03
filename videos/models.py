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
    """
    Main video model
    """
    QUALITY_CHOICES = [
        ('120p', '120p'),
        ('360p', '360p'),
        ('720p', '720p'),
        ('1080p', '1080p'),
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
        help_text=_('Video thumbnail image')
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='videos',
        help_text=_('Video genre')
    )
    duration = models.DurationField(
        help_text=_('Video duration')
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
