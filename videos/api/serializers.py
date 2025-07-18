from rest_framework import serializers
from ..models import Video, Genre, VideoQuality, WatchProgress
from ..utils import is_video_file


class GenreSerializer(serializers.ModelSerializer):
    """
    Serializer for video genres.
    """
    class Meta:
        model = Genre
        fields = ['id', 'name', 'slug']
        read_only_fields = ['slug']


class VideoQualitySerializer(serializers.ModelSerializer):
    """
    Serializer for video quality versions.
    """
    class Meta:
        model = VideoQuality
        fields = ['quality', 'file_size', 'is_ready']


class VideoListSerializer(serializers.ModelSerializer):
    """
    Serializer for video list view.
    """
    genre = GenreSerializer(read_only=True)
    category = serializers.CharField(source='genre.name', read_only=True)
    thumbnail_url = serializers.SerializerMethodField()
    video_file = serializers.SerializerMethodField()
    
    class Meta:
        model = Video
        fields = [
            'id', 'title', 'description', 'genre', 'category',
            'thumbnail_url', 'video_file', 'duration', 'created_at'
        ]
    
    def get_thumbnail_url(self, obj):
        """Return absolute URL for thumbnail."""
        request = self.context.get('request')
        thumbnail_url = obj.thumbnail_url
        if request and thumbnail_url:
            return request.build_absolute_uri(thumbnail_url)
        return thumbnail_url
    
    def get_video_file(self, obj):
        """Return absolute URL for video file."""
        request = self.context.get('request')
        if request and obj.video_file:
            return request.build_absolute_uri(obj.video_file.url)
        return obj.video_file.url if obj.video_file else None


class VideoDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for video detail view.
    """
    genre = GenreSerializer(read_only=True)
    category = serializers.CharField(source='genre.name', read_only=True)
    qualities = VideoQualitySerializer(many=True, read_only=True)
    thumbnail_url = serializers.SerializerMethodField()
    video_file = serializers.SerializerMethodField()
    
    class Meta:
        model = Video
        fields = [
            'id', 'title', 'description', 'genre', 'category', 'thumbnail_url',
            'video_file', 'duration', 'is_processed', 'qualities', 'created_at'
        ]
    
    def get_thumbnail_url(self, obj):
        """Return absolute URL for thumbnail."""
        request = self.context.get('request')
        thumbnail_url = obj.thumbnail_url
        if request and thumbnail_url:
            return request.build_absolute_uri(thumbnail_url)
        return thumbnail_url
    
    def get_video_file(self, obj):
        """Return absolute URL for video file."""
        request = self.context.get('request')
        if request and obj.video_file:
            return request.build_absolute_uri(obj.video_file.url)
        return obj.video_file.url if obj.video_file else None


class VideoUploadSerializer(serializers.ModelSerializer):
    """
    Serializer for video upload.
    """
    genre_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Video
        fields = ['title', 'description', 'genre_id', 'video_file', 'thumbnail']
    
    def validate_video_file(self, value):
        """Validate video file format."""
        if not is_video_file(value.name):
            raise serializers.ValidationError(
                "Unsupported video format. Please upload MP4, AVI, MOV, MKV, WMV, FLV, or WebM files."
            )
        
        # Check file size (max 500MB)
        max_size = 500 * 1024 * 1024  # 500MB in bytes
        if value.size > max_size:
            raise serializers.ValidationError(
                "Video file too large. Maximum size is 500MB."
            )
        
        return value
    
    def validate_genre_id(self, value):
        """Validate genre exists."""
        try:
            Genre.objects.get(id=value)
        except Genre.DoesNotExist:
            raise serializers.ValidationError("Invalid genre selected.")
        
        return value
    
    def create(self, validated_data):
        """Create video with genre."""
        genre_id = validated_data.pop('genre_id')
        genre = Genre.objects.get(id=genre_id)
        validated_data['genre'] = genre
        
        return super().create(validated_data)


class WatchProgressSerializer(serializers.ModelSerializer):
    """
    Serializer for watch progress.
    """
    progress_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = WatchProgress
        fields = [
            'video', 'current_time', 'is_completed', 
            'progress_percentage', 'last_watched'
        ]
        read_only_fields = ['last_watched']


class DashboardSerializer(serializers.Serializer):
    """
    Serializer for dashboard data.
    """
    hero_video = VideoDetailSerializer(read_only=True)
    genres = serializers.SerializerMethodField()
    continue_watching = serializers.SerializerMethodField()
    
    def get_genres(self, obj):
        """Get videos grouped by genre."""
        genres_data = []
        for genre in Genre.objects.all():
            videos = Video.objects.filter(
                genre=genre, 
                is_processed=True
            ).order_by('-created_at')[:10]
            
            if videos.exists():
                genres_data.append({
                    'genre': GenreSerializer(genre).data,
                    'videos': VideoListSerializer(videos, many=True).data
                })
        
        return genres_data
    
    def get_continue_watching(self, obj):
        """Get user's continue watching list."""
        user = self.context.get('user')
        if not user or not user.is_authenticated:
            return []
        
        progress_list = WatchProgress.objects.filter(
            user=user, 
            is_completed=False,
            current_time__gt=0
        ).select_related('video').order_by('-last_watched')[:5]
        
        return [{
            'video': VideoListSerializer(p.video).data,
            'progress': WatchProgressSerializer(p).data
        } for p in progress_list]
