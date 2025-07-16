"""
Video views for Videoflix application
"""
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Video, Genre, WatchProgress
from .serializers import (
    VideoListSerializer,
    VideoDetailSerializer,
    GenreSerializer,
    WatchProgressSerializer,
    WatchProgressUpdateSerializer,
    VideoUploadSerializer
)
from .utils import get_video_quality_recommendations


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
        Return featured videos, or first 5 videos if none are featured
        """
        featured_videos = Video.objects.filter(is_featured=True)
        
        # If no videos are marked as featured, return first 5 videos
        if not featured_videos.exists():
            return Video.objects.all()[:5]
        
        return featured_videos


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
        
        # TODO: Add background video processing if needed
        # For now, video processing is handled synchronously
        
        return video


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def video_stream_view(request, video_id, quality):
    """
    Stream video file with specific quality - No authentication required for video streaming
    Support for HTTP Range requests for proper video seeking
    """
    from django.http import HttpResponseRedirect, Http404, FileResponse, HttpResponse
    import os
    import re

    def get_video_or_404(video_id):
        try:
            return Video.objects.get(id=video_id)
        except Video.DoesNotExist:
            raise Http404("Video not found")

    def get_video_file(video, quality):
        video_file = video.video_files.filter(quality=quality).first()
        if not video_file:
            default_quality = video.get_default_quality()
            if default_quality:
                video_file = video.video_files.filter(quality=default_quality).first()
        return video_file

    def serve_video_with_range_support(file_path, request):
        """
        Serve video file with HTTP Range request support for seeking
        """
        file_size = os.path.getsize(file_path)
        
        # Check if client supports range requests
        range_header = request.META.get('HTTP_RANGE', '').strip()
        
        if range_header:
            # Parse range header
            range_match = re.search(r'bytes=(\d+)-(\d*)', range_header)
            
            if range_match:
                start = int(range_match.group(1))
                end = int(range_match.group(2)) if range_match.group(2) else file_size - 1
                
                # Ensure valid range
                if start >= file_size or end >= file_size:
                    response = HttpResponse(status=416)  # Range Not Satisfiable
                    response['Content-Range'] = f'bytes */{file_size}'
                    return response
                
                # Create partial content response
                with open(file_path, 'rb') as f:
                    f.seek(start)
                    chunk = f.read(end - start + 1)
                
                response = HttpResponse(
                    chunk,
                    status=206,  # Partial Content
                    content_type='video/mp4'
                )
                response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
                response['Content-Length'] = str(end - start + 1)
                response['Accept-Ranges'] = 'bytes'
                return response
        
        # Serve full file if no range request
        response = FileResponse(
            open(file_path, 'rb'),
            content_type='video/mp4'
        )
        response['Content-Length'] = file_size
        response['Accept-Ranges'] = 'bytes'
        return response

    video = get_video_or_404(video_id)
    video_file = get_video_file(video, quality)

    if not video_file or not video_file.file:
        raise Http404("Video file not found")

    file_path = str(video_file.file)
    if file_path.startswith('http://') or file_path.startswith('https://'):
        return HttpResponseRedirect(file_path)
    else:
        if not os.path.exists(video_file.file.path):
            raise Http404("Video file not found on disk")
        
        return serve_video_with_range_support(video_file.file.path, request)


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
        try:
            watch_progress = self.get_object()
            print(f"DEBUG: Received data: {request.data}")
            print(f"DEBUG: Watch progress object: {watch_progress}")
            
            serializer = self.get_serializer(watch_progress, data=request.data)
            print(f"DEBUG: Serializer validation...")
            
            if not serializer.is_valid():
                print(f"DEBUG: Serializer errors: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.is_valid(raise_exception=True)
            
            # Auto-set completed if video is watched to >=90%
            progress_seconds = serializer.validated_data.get('progress_seconds', 0)
            if watch_progress.video.duration and progress_seconds > 0:
                total_seconds = watch_progress.video.duration.total_seconds()
                if total_seconds > 0:
                    progress_percentage = (progress_seconds / total_seconds) * 100
                    if progress_percentage >= 90:
                        serializer.validated_data['completed'] = True
            
            result = serializer.save()
            print(f"DEBUG: Saved successfully: {result}")
            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"DEBUG: Exception in post method: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def videos_by_genre_view(request):
    """
    Get videos grouped by genre
    """
    genres = Genre.objects.prefetch_related('videos').all()
    result = []
    
    for genre in genres:
        videos_queryset = genre.videos.all()
        if videos_queryset.exists():  # Only include genres that have videos
            videos = videos_queryset[:10]  # Limit to 10 videos per genre
            genre_data = {
                'id': genre.id,
                'name': genre.name,
                'description': genre.description,
                'videos': VideoListSerializer(videos, many=True).data
            }
            result.append(genre_data)
    
    return Response(result)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def continue_watching_view(request):
    """
    Get videos user can continue watching (not completed and progress > 0)
    """
    # Get all watch progress with progress > 0, not completed, ordered by most recent
    continue_watching = WatchProgress.objects.filter(
        user=request.user,
        progress_seconds__gt=0,
        completed=False
    ).order_by('-last_watched')[:10]
    
    serializer = WatchProgressSerializer(continue_watching, many=True)
    return Response(serializer.data)
    return Response(serializer.data)
