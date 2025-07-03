"""
Video views for Videoflix application
"""
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django_rq import get_queue

from .models import Video, Genre, WatchProgress
from .serializers import (
    VideoListSerializer,
    VideoDetailSerializer,
    GenreSerializer,
    WatchProgressSerializer,
    WatchProgressUpdateSerializer,
    VideoUploadSerializer
)
from .utils import process_video_upload, get_video_quality_recommendations


class GenreListView(generics.ListAPIView):
    """
    List all genres
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticated]


class VideoListView(generics.ListAPIView):
    """
    List videos with filtering and search
    """
    serializer_class = VideoListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter videos by genre and search query
        """
        queryset = Video.objects.all()
        
        # Filter by genre
        genre_id = self.request.query_params.get('genre', None)
        if genre_id is not None:
            queryset = queryset.filter(genre_id=genre_id)
        
        # Search by title and description
        search = self.request.query_params.get('search', None)
        if search is not None:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search)
            )
        
        return queryset


class VideoDetailView(generics.RetrieveAPIView):
    """
    Retrieve video details
    """
    queryset = Video.objects.all()
    serializer_class = VideoDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class FeaturedVideosView(generics.ListAPIView):
    """
    List featured videos for homepage
    """
    serializer_class = VideoListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Return only featured videos
        """
        return Video.objects.filter(is_featured=True)


class VideoUploadView(generics.CreateAPIView):
    """
    Upload new video
    """
    serializer_class = VideoUploadSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        """
        Create video and queue for processing
        """
        video = serializer.save()
        
        # Queue video for background processing
        queue = get_queue('default')
        queue.enqueue(process_video_upload, video.id)
        
        return video


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def video_stream_view(request, video_id, quality):
    """
    Stream video file with specific quality
    """
    video = get_object_or_404(Video, id=video_id)
    
    # Get video file for requested quality
    video_file = video.video_files.filter(quality=quality).first()
    
    if not video_file:
        # Fallback to default quality
        default_quality = video.get_default_quality()
        if default_quality:
            video_file = video.video_files.filter(quality=default_quality).first()
    
    if not video_file:
        return Response(
            {'error': 'Video file not available'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    return Response({
        'video_url': video_file.file.url,
        'quality': video_file.quality,
        'file_size': video_file.file_size
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def video_quality_options_view(request, video_id):
    """
    Get available quality options for video
    """
    video = get_object_or_404(Video, id=video_id)
    
    video_files = video.video_files.filter(is_processed=True)
    qualities = []
    
    for video_file in video_files:
        qualities.append({
            'quality': video_file.quality,
            'file_size': video_file.file_size
        })
    
    # Get recommended quality
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    recommended_quality = get_video_quality_recommendations(user_agent)
    
    return Response({
        'available_qualities': qualities,
        'recommended_quality': recommended_quality
    })


class WatchProgressListView(generics.ListAPIView):
    """
    List user's watch progress
    """
    serializer_class = WatchProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Return only current user's watch progress
        """
        return WatchProgress.objects.filter(
            user=self.request.user,
            progress_seconds__gt=0
        ).order_by('-last_watched')


class WatchProgressUpdateView(generics.CreateAPIView, generics.UpdateAPIView):
    """
    Create or update watch progress
    """
    serializer_class = WatchProgressUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """
        Get or create watch progress for user and video
        """
        video_id = self.kwargs.get('video_id')
        video = get_object_or_404(Video, id=video_id)
        
        watch_progress, created = WatchProgress.objects.get_or_create(
            user=self.request.user,
            video=video,
            defaults={'progress_seconds': 0}
        )
        
        return watch_progress
    
    def post(self, request, *args, **kwargs):
        """
        Create or update watch progress
        """
        watch_progress = self.get_object()
        serializer = self.get_serializer(watch_progress, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def videos_by_genre_view(request):
    """
    Get videos grouped by genre
    """
    genres = Genre.objects.prefetch_related('videos').all()
    result = []
    
    for genre in genres:
        videos = genre.videos.all()[:10]  # Limit to 10 videos per genre
        genre_data = {
            'genre': GenreSerializer(genre).data,
            'videos': VideoListSerializer(videos, many=True).data
        }
        result.append(genre_data)
    
    return Response(result)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def continue_watching_view(request):
    """
    Get videos user can continue watching
    """
    continue_watching = WatchProgress.objects.filter(
        user=request.user,
        completed=False,
        progress_seconds__gt=0
    ).order_by('-last_watched')[:10]
    
    serializer = WatchProgressSerializer(continue_watching, many=True)
    return Response(serializer.data)
