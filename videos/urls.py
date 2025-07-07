"""
URL configuration for videos app
"""
from django.urls import path
from .views import (
    GenreListView,
    VideoListView,
    VideoDetailView,
    FeaturedVideosView,
    VideoUploadView,
    video_stream_view,
    video_quality_options_view,
    WatchProgressListView,
    WatchProgressUpdateView,
    videos_by_genre_view,
    continue_watching_view
)

app_name = 'videos'

urlpatterns = [
    # Genre endpoints
    path('genres/', GenreListView.as_view(), name='genre_list'),
    
    # Video endpoints
    path('', VideoListView.as_view(), name='video_list'),
    path('featured/', FeaturedVideosView.as_view(), name='featured_videos'),
    path('by-genre/', videos_by_genre_view, name='videos_by_genre'),
    path('upload/', VideoUploadView.as_view(), name='video_upload'),
    path('<int:pk>/', VideoDetailView.as_view(), name='video_detail'),
    
    # Video streaming endpoints
    path('<int:video_id>/stream/<str:quality>/', video_stream_view, name='video_stream'),
    
    # Watch progress endpoints
    path('progress/', WatchProgressListView.as_view(), name='watch_progress_list'),
    path('<int:video_id>/progress/', WatchProgressUpdateView.as_view(), name='watch_progress_update'),
    path('continue-watching/', continue_watching_view, name='continue_watching'),
]
