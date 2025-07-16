"""
Admin configuration for videos app
"""
from django.contrib import admin
from django import forms
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
    readonly_fields = ('created_at', 'updated_at', 'duration', 'thumbnail')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'genre')
        }),
        ('Media', {
            'fields': ('thumbnail',)
        }),
        ('Settings', {
            'fields': ('is_featured',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )



# Inline für VideoFile
from django.contrib.admin import TabularInline


# Eigenes ModelForm für VideoFileInline, damit file_size automatisch gesetzt wird
class VideoFileInlineForm(forms.ModelForm):
    class Meta:
        model = VideoFile
        fields = ['file']  # quality nicht auswählbar

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Qualität immer auf 'original' setzen
        instance.quality = 'original'
        # file_size setzen
        if instance.file and hasattr(instance.file, 'size'):
            instance.file_size = instance.file.size
        elif instance.file and hasattr(instance.file, 'file'):
            instance.file_size = instance.file.file.size
        else:
            instance.file_size = 0
        if commit:
            instance.save()
        return instance

class VideoFileInline(TabularInline):
    model = VideoFile
    form = VideoFileInlineForm
    extra = 1
    readonly_fields = ('file_size', 'created_at', 'quality', 'is_processed')
    fields = ('file', 'quality', 'file_size', 'is_processed', 'created_at')
    can_delete = True

# VideoAdmin um Inline erweitern
VideoAdmin.inlines = [VideoFileInline]


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
