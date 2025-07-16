"""
Serializers for videos app
"""
from rest_framework import serializers
from .models import Video, VideoFile, Genre, WatchProgress


class GenreSerializer(serializers.ModelSerializer):
    """
    Serializer for Genre model
    """
    class Meta:
        model = Genre
        fields = ['id', 'name', 'description']


class VideoFileSerializer(serializers.ModelSerializer):
    """
    Serializer for VideoFile model
    """
    file = serializers.SerializerMethodField()
    
    class Meta:
        model = VideoFile
        fields = ['id', 'quality', 'file', 'file_size', 'is_processed']
    
    def get_file(self, obj):
        """
        Return streaming URL for proper Range Request support
        """
        from django.urls import reverse
        from django.conf import settings
        
        # Use the streaming endpoint for proper Range Request support
        # This ensures all video requests go through our video_stream_view
        relative_url = reverse('videos:video_stream', kwargs={
            'video_id': obj.video.id,
            'quality': obj.quality
        })
        
        # Return absolute URL to avoid /api/ prefix
        return f"http://localhost:8000{relative_url}"


class VideoListSerializer(serializers.ModelSerializer):
    """
    Serializer for video list view
    """
    genre = GenreSerializer(read_only=True)
    video_files = VideoFileSerializer(many=True, read_only=True)
    thumbnail = serializers.SerializerMethodField()
    
    class Meta:
        model = Video
        fields = [
            'id', 
            'title', 
            'description', 
            'thumbnail', 
            'genre', 
            'duration', 
            'age_rating',
            'created_at',
            'is_featured',
            'video_files'
        ]
    
    def get_thumbnail(self, obj):
        """
        Return thumbnail URL - prefer uploaded image, fallback to external URL
        """
        if obj.thumbnail:
            return obj.thumbnail.url
        elif getattr(obj, 'thumbnail_url', None):
            return getattr(obj, 'thumbnail_url', None)
        return None


class VideoDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for video detail view
    """
    genre = GenreSerializer(read_only=True)
    video_files = VideoFileSerializer(many=True, read_only=True)
    thumbnail = serializers.SerializerMethodField()
    
    class Meta:
        model = Video
        fields = [
            'id',
            'title',
            'description',
            'thumbnail',
            'genre',
            'duration',
            'age_rating',
            'created_at',
            'updated_at',
            'is_featured',
            'video_files'
        ]
    
    def get_thumbnail(self, obj):
        """
        Return thumbnail URL - prefer uploaded image, fallback to external URL
        """
        if obj.thumbnail:
            return obj.thumbnail.url
        elif getattr(obj, 'thumbnail_url', None):
            return getattr(obj, 'thumbnail_url', None)
        return None


class WatchProgressSerializer(serializers.ModelSerializer):
    """
    Serializer for WatchProgress model
    """
    video = VideoListSerializer(read_only=True)
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = WatchProgress
        fields = [
            'id',
            'video',
            'progress_seconds',
            'progress_percentage',
            'last_resolution',
            'last_watched',
            'completed'
        ]
    
    def get_progress_percentage(self, obj):
        """
        Get progress percentage
        """
        return obj.get_progress_percentage()


class WatchProgressUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating watch progress
    """
    class Meta:
        model = WatchProgress
        fields = ['progress_seconds', 'last_resolution', 'completed']
    
    def validate_last_resolution(self, value):
        """
        Validate and convert resolution values
        """
        if value == 'original':
            # Convert 'original' to highest available quality
            return '1080p'
        return value


class VideoUploadSerializer(serializers.ModelSerializer):
    """
    Serializer for video upload
    """
    video_file = serializers.FileField(write_only=True)
    genre_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Video
        fields = [
            'title',
            'description',
            'genre_id',
            'video_file',
            'is_featured'
        ]
    
    def validate_video_file(self, value):
        """
        Validate video file
        """
        max_size = 500 * 1024 * 1024  # 500MB
        if value.size > max_size:
            raise serializers.ValidationError(
                "Video file size cannot exceed 500MB"
            )
        
        allowed_extensions = ['mp4', 'avi', 'mov', 'wmv']
        extension = value.name.split('.')[-1].lower()
        if extension not in allowed_extensions:
            raise serializers.ValidationError(
                f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
            )
        
        return value
    
    def create(self, validated_data):
        """
        Create video and initial video file
        """
        video_file = validated_data.pop('video_file')
        genre_id = validated_data.pop('genre_id')
        
        try:
            genre = Genre.objects.get(id=genre_id)
        except Genre.DoesNotExist:
            raise serializers.ValidationError("Invalid genre ID")
        
        validated_data['genre'] = genre
        video = Video.objects.create(**validated_data)
        
        # Create initial video file (original quality)
        VideoFile.objects.create(
            video=video,
            quality='original',
            file=video_file,
            file_size=video_file.size,
            is_processed=False
        )
        
        return video
