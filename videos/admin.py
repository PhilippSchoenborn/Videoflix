"""
Admin configuration for videos app
"""
from django.contrib import admin
from .models import Genre, Video, VideoFile, WatchProgress


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """
    Admin configuration for Genre
    """
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """
    Admin configuration for Video
    """
    list_display = ('title', 'genre', 'duration', 'is_featured', 'created_at')
    list_filter = ('genre', 'is_featured', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'genre')
        }),
        ('Media', {
            'fields': ('thumbnail',)
        }),
        ('Settings', {
            'fields': ('is_featured', 'duration')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(VideoFile)
class VideoFileAdmin(admin.ModelAdmin):
    """
    Admin configuration for VideoFile
    """
    list_display = ('video', 'quality', 'file_size', 'is_processed', 'created_at')
    list_filter = ('quality', 'is_processed', 'created_at')
    search_fields = ('video__title',)
    ordering = ('-created_at',)
    readonly_fields = ('file_size', 'created_at')


@admin.register(WatchProgress)
class WatchProgressAdmin(admin.ModelAdmin):
    """
    Admin configuration for WatchProgress
    """
    list_display = ('user', 'video', 'progress_seconds', 'completed', 'last_watched')
    list_filter = ('completed', 'last_watched')
    search_fields = ('user__email', 'video__title')
    ordering = ('-last_watched',)
    readonly_fields = ('last_watched',)
