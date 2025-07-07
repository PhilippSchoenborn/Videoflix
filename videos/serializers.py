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
        Return direct URL for external files, otherwise use default file URL
        """
        file_str = str(obj.file)
        # If it's an external URL that got mangled by Django's FileField
        if 'commondatastorage.googleapis.com' in file_str:
            # Extract the actual URL
            if 'https%3A/' in file_str:
                # URL encoded version
                return file_str.replace('/media/https%3A/', 'https://').replace('%3A/', '://')
            elif 'https://' in file_str:
                # Direct URL
                return file_str.split('/media/')[-1] if '/media/' in file_str else file_str
            else:
                # Try to reconstruct the URL
                return f"https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/{file_str.split('/')[-1]}"
        # For local files, use the default behavior
        return obj.file.url if obj.file else None


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
