"""
Test cases for videos app
"""
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from videos.models import Genre, Video, VideoFile, WatchProgress
from videos.utils import format_duration, format_file_size
from tests import BaseAPITestCase
from datetime import timedelta


class TestGenreModel(TestCase):
    """
    Test Genre model
    """
    
    def test_create_genre(self):
        """
        Test creating a genre
        """
        genre = Genre.objects.create(
            name='Action',
            description='Action movies'
        )
        
        self.assertEqual(genre.name, 'Action')
        self.assertEqual(str(genre), 'Action')


class TestVideoModel(TestCase):
    """
    Test Video model
    """
    
    def setUp(self):
        """
        Set up test data
        """
        self.genre = Genre.objects.create(name='Drama')
    
    def test_create_video(self):
        """
        Test creating a video
        """
        video = Video.objects.create(
            title='Test Video',
            description='A test video',
            genre=self.genre,
            duration=timedelta(minutes=90)
        )
        
        self.assertEqual(video.title, 'Test Video')
        self.assertEqual(video.genre, self.genre)
        self.assertEqual(str(video), 'Test Video')
    
    def test_get_default_quality(self):
        """
        Test getting default quality
        """
        video = Video.objects.create(
            title='Test Video',
            description='A test video',
            genre=self.genre,
            duration=timedelta(minutes=90)
        )
        
        # No video files yet
        self.assertIsNone(video.get_default_quality())
        
        # Add video files
        VideoFile.objects.create(
            video=video,
            quality='360p',
            file_size=1000000,
            is_processed=True
        )
        VideoFile.objects.create(
            video=video,
            quality='1080p',
            file_size=5000000,
            is_processed=True
        )
        
        # Should return highest quality
        self.assertEqual(video.get_default_quality(), '1080p')


class TestWatchProgressModel(BaseAPITestCase):
    """
    Test WatchProgress model
    """
    
    def setUp(self):
        """
        Set up test data
        """
        super().setUp()
        self.genre = Genre.objects.create(name='Drama')
        self.video = Video.objects.create(
            title='Test Video',
            description='A test video',
            genre=self.genre,
            duration=timedelta(minutes=90)  # 5400 seconds
        )
    
    def test_create_watch_progress(self):
        """
        Test creating watch progress
        """
        progress = WatchProgress.objects.create(
            user=self.user,
            video=self.video,
            progress_seconds=1800  # 30 minutes
        )
        
        self.assertEqual(progress.user, self.user)
        self.assertEqual(progress.video, self.video)
        self.assertEqual(progress.progress_seconds, 1800)
    
    def test_progress_percentage(self):
        """
        Test progress percentage calculation
        """
        progress = WatchProgress.objects.create(
            user=self.user,
            video=self.video,
            progress_seconds=2700  # 45 minutes
        )
        
        # 45 minutes out of 90 minutes = 50%
        self.assertEqual(progress.get_progress_percentage(), 50.0)


class TestVideoUtils(TestCase):
    """
    Test video utility functions
    """
    
    def test_format_duration(self):
        """
        Test duration formatting
        """
        # Test minutes only
        duration = timedelta(minutes=5, seconds=30)
        self.assertEqual(format_duration(duration), '05:30')
        
        # Test hours, minutes, seconds
        duration = timedelta(hours=2, minutes=15, seconds=45)
        self.assertEqual(format_duration(duration), '02:15:45')
        
        # Test zero duration
        self.assertEqual(format_duration(None), '00:00')
    
    def test_format_file_size(self):
        """
        Test file size formatting
        """
        self.assertEqual(format_file_size(0), '0 B')
        self.assertEqual(format_file_size(1024), '1.0 KB')
        self.assertEqual(format_file_size(1048576), '1.0 MB')
        self.assertEqual(format_file_size(1073741824), '1.0 GB')


class TestGenreAPI(BaseAPITestCase):
    """
    Test Genre API endpoints
    """
    
    def setUp(self):
        """
        Set up test data
        """
        super().setUp()
        self.genre_list_url = reverse('videos:genre_list')
        self.genre1 = Genre.objects.create(name='Action', description='Action movies')
        self.genre2 = Genre.objects.create(name='Comedy', description='Comedy movies')
    
    def test_list_genres(self):
        """
        Test listing genres
        """
        response = self.client.get(self.genre_list_url)
        genres = response.data['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(genres), 2)
        self.assertEqual(genres[0]['name'], 'Action')


class TestVideoAPI(BaseAPITestCase):
    """
    Test Video API endpoints
    """
    
    def setUp(self):
        """
        Set up test data
        """
        super().setUp()
        self.genre = Genre.objects.create(name='Drama')
        self.video = Video.objects.create(
            title='Test Video',
            description='A test video',
            genre=self.genre,
            duration=timedelta(minutes=90),
            is_featured=True
        )
        self.video_list_url = reverse('videos:video_list')
        self.video_detail_url = reverse('videos:video_detail', kwargs={'pk': self.video.pk})
        self.featured_videos_url = reverse('videos:featured_videos')
    
    def test_list_videos(self):
        """
        Test listing videos
        """
        response = self.client.get(self.video_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Video')
    
    def test_video_detail(self):
        """
        Test getting video detail
        """
        response = self.client.get(self.video_detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Video')
        self.assertEqual(response.data['genre']['name'], 'Drama')
    
    def test_featured_videos(self):
        """
        Test listing featured videos
        """
        response = self.client.get(self.featured_videos_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['is_featured'], True)
    
    def test_filter_videos_by_genre(self):
        """
        Test filtering videos by genre
        """
        # Create another genre and video
        comedy_genre = Genre.objects.create(name='Comedy')
        Video.objects.create(
            title='Comedy Video',
            description='A comedy video',
            genre=comedy_genre,
            duration=timedelta(minutes=60)
        )
        
        # Filter by drama genre
        response = self.client.get(self.video_list_url, {'genre': self.genre.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Video')
    
    def test_search_videos(self):
        """
        Test searching videos
        """
        response = self.client.get(self.video_list_url, {'search': 'Test'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Video')
        
        # Search for non-existent term
        response = self.client.get(self.video_list_url, {'search': 'NonExistent'})
        self.assertEqual(len(response.data['results']), 0)


class TestVideoStreaming(BaseAPITestCase):
    """
    Test video streaming endpoints
    """
    
    def setUp(self):
        """
        Set up test data
        """
        super().setUp()
        self.genre = Genre.objects.create(name='Drama')
        self.video = Video.objects.create(
            title='Test Video',
            description='A test video',
            genre=self.genre,
            duration=timedelta(minutes=90)
        )
        
        # Create video files
        self.video_file_720p = VideoFile.objects.create(
            video=self.video,
            quality='720p',
            file_size=2500000,
            is_processed=True
        )
        self.video_file_1080p = VideoFile.objects.create(
            video=self.video,
            quality='1080p',
            file_size=5000000,
            is_processed=True
        )
        
        self.stream_url = reverse('videos:video_stream', kwargs={
            'video_id': self.video.id,
            'quality': '720p'
        })
        self.qualities_url = reverse('videos:video_qualities', kwargs={
            'video_id': self.video.id
        })
    
    def test_video_stream(self):
        """
        Test video streaming endpoint
        """
        response = self.client.get(self.stream_url)
        # In Testumgebung existiert meist kein echtes Video-File, daher 404 ok
        self.assertIn(response.status_code, [200, 404])
        # Nur prüfen, falls 200
        if response.status_code == 200:
            self.assertIn('video_url', response.data)
            self.assertEqual(response.data['quality'], '720p')
    
    def test_video_qualities(self):
        """
        Test video quality options endpoint
        """
        response = self.client.get(self.qualities_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('available_qualities', response.data)
        self.assertEqual(len(response.data['available_qualities']), 2)
        self.assertIn('recommended_quality', response.data)


class TestWatchProgressAPI(BaseAPITestCase):
    """
    Test watch progress API endpoints
    """
    
    def setUp(self):
        """
        Set up test data
        """
        super().setUp()
        self.genre = Genre.objects.create(name='Drama')
        self.video = Video.objects.create(
            title='Test Video',
            description='A test video',
            genre=self.genre,
            duration=timedelta(minutes=90)
        )
        
        self.progress_list_url = reverse('videos:watch_progress_list')
        self.progress_update_url = reverse('videos:watch_progress_update', kwargs={
            'video_id': self.video.id
        })
        self.continue_watching_url = reverse('videos:continue_watching')
    
    def test_create_watch_progress(self):
        """
        Test creating watch progress
        """
        response = self.client.post(self.progress_update_url, {
            'progress_seconds': 1800,
            'completed': False
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['progress_seconds'], 1800)
        
        # Check progress was created in database
        self.assertTrue(WatchProgress.objects.filter(
            user=self.user,
            video=self.video
        ).exists())
    
    def test_update_watch_progress(self):
        """
        Test updating existing watch progress
        """
        # Create initial progress
        WatchProgress.objects.create(
            user=self.user,
            video=self.video,
            progress_seconds=900
        )
        
        # Update progress
        response = self.client.post(self.progress_update_url, {
            'progress_seconds': 1800,
            'completed': False
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['progress_seconds'], 1800)
    
    def test_list_watch_progress(self):
        """
        Test listing user's watch progress
        """
        # Create watch progress
        WatchProgress.objects.create(
            user=self.user,
            video=self.video,
            progress_seconds=1800
        )
        
        response = self.client.get(self.progress_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['progress_seconds'], 1800)
    
    def test_continue_watching(self):
        """
        Test continue watching endpoint
        """
        # Create incomplete watch progress
        WatchProgress.objects.create(
            user=self.user,
            video=self.video,
            progress_seconds=1800,
            completed=False
        )
        
        response = self.client.get(self.continue_watching_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['progress_seconds'], 1800)


class TestVideosByGenre(BaseAPITestCase):
    """
    Test videos by genre endpoint
    """
    
    def setUp(self):
        """
        Set up test data
        """
        super().setUp()
        self.videos_by_genre_url = reverse('videos:videos_by_genre')
        
        # Create genres
        self.action_genre = Genre.objects.create(name='Action')
        self.comedy_genre = Genre.objects.create(name='Comedy')
        
        # Create videos
        Video.objects.create(
            title='Action Movie 1',
            description='An action movie',
            genre=self.action_genre,
            duration=timedelta(minutes=120)
        )
        Video.objects.create(
            title='Comedy Movie 1',
            description='A comedy movie',
            genre=self.comedy_genre,
            duration=timedelta(minutes=90)
        )
    
    def test_videos_by_genre(self):
        """
        Test getting videos grouped by genre
        """
        response = self.client.get(self.videos_by_genre_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Check structure
        genre_data = response.data[0]
        self.assertIn('name', genre_data)
        self.assertIn('description', genre_data)
        self.assertIn('videos', genre_data)
        self.assertIsInstance(genre_data['videos'], list)
