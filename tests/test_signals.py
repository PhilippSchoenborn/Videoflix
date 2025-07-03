"""
Test cases for Django signals
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from authentication.models import EmailVerificationToken, PasswordResetToken
from videos.models import Video, VideoFile, Genre, WatchProgress
from datetime import timedelta
import tempfile
import logging

User = get_user_model()


class AuthenticationSignalsTest(TestCase):
    """
    Test authentication app signals
    """
    
    def setUp(self):
        """
        Set up test data
        """
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'TestPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
    
    def test_user_creation_signal(self):
        """
        Test that signal is triggered when user is created
        """
        # Capture log output
        with self.assertLogs('authentication.signals', level='INFO') as log:
            user = User.objects.create_user(**self.user_data)
            
        # Check that signal was triggered
        self.assertIn(f'New user created: {user.email}', log.output[0])
        
        # Check that email verification token was created
        self.assertTrue(
            EmailVerificationToken.objects.filter(user=user).exists()
        )
    
    def test_email_verification_token_creation_signal(self):
        """
        Test that signal is triggered when email verification token is created
        """
        user = User.objects.create_user(**self.user_data)
        
        with self.assertLogs('authentication.signals', level='INFO') as log:
            EmailVerificationToken.objects.create(user=user)
            
        self.assertIn(f'Email verification token created for user: {user.email}', log.output[0])
    
    def test_password_reset_token_creation_signal(self):
        """
        Test that signal is triggered when password reset token is created
        """
        user = User.objects.create_user(**self.user_data)
        
        with self.assertLogs('authentication.signals', level='INFO') as log:
            PasswordResetToken.objects.create(user=user)
            
        self.assertIn(f'Password reset token created for user: {user.email}', log.output[0])
    
    def test_user_deletion_signal(self):
        """
        Test that signal is triggered when user is deleted
        """
        user = User.objects.create_user(**self.user_data)
        user_email = user.email
        
        with self.assertLogs('authentication.signals', level='WARNING') as log:
            user.delete()
            
        self.assertIn(f'User deletion initiated: {user_email}', log.output[0])


class VideosSignalsTest(TestCase):
    """
    Test videos app signals
    """
    
    def setUp(self):
        """
        Set up test data
        """
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='TestPass123!'
        )
        self.genre = Genre.objects.create(name='Test Genre')
    
    def test_video_creation_signal(self):
        """
        Test that signal is triggered when video is created
        """
        # Create a temporary video file
        video_file = SimpleUploadedFile(
            "test_video.mp4",
            b"fake video content",
            content_type="video/mp4"
        )
        
        with self.assertLogs('videos.signals', level='INFO') as log:
            video = Video.objects.create(
                title='Test Video',
                description='Test Description',
                user=self.user,
                video_file=video_file,
                duration=timedelta(minutes=5)
            )
            
        self.assertIn(f'New video created: {video.title}', log.output[0])
        
        # Check that video is marked as not processed
        video.refresh_from_db()
        self.assertFalse(video.is_processed)
    
    def test_video_file_creation_signal(self):
        """
        Test that signal is triggered when video file is created
        """
        video = Video.objects.create(
            title='Test Video',
            description='Test Description',
            user=self.user,
            duration=timedelta(minutes=5)
        )
        
        video_file = SimpleUploadedFile(
            "test_720p.mp4",
            b"fake video content",
            content_type="video/mp4"
        )
        
        with self.assertLogs('videos.signals', level='INFO') as log:
            VideoFile.objects.create(
                video=video,
                quality='720p',
                file=video_file
            )
            
        self.assertIn('New video file created: 720p quality', log.output[0])
    
    def test_watch_progress_creation_signal(self):
        """
        Test that signal is triggered when watch progress is created
        """
        video = Video.objects.create(
            title='Test Video',
            description='Test Description',
            user=self.user,
            duration=timedelta(minutes=10)
        )
        
        with self.assertLogs('videos.signals', level='INFO') as log:
            WatchProgress.objects.create(
                user=self.user,
                video=video,
                current_time=timedelta(minutes=2)
            )
            
        self.assertIn(f'Watch progress started: User {self.user.email} started watching', log.output[0])
    
    def test_genre_creation_signal(self):
        """
        Test that signal is triggered when genre is created
        """
        with self.assertLogs('videos.signals', level='INFO') as log:
            Genre.objects.create(name='Action')
            
        self.assertIn('New genre created: Action', log.output[0])
    
    def test_video_deletion_signal(self):
        """
        Test that signal is triggered when video is deleted
        """
        video = Video.objects.create(
            title='Test Video',
            description='Test Description',
            user=self.user,
            duration=timedelta(minutes=5)
        )
        video_title = video.title
        
        with self.assertLogs('videos.signals', level='WARNING') as log:
            video.delete()
            
        self.assertIn(f'Video deletion initiated: {video_title}', log.output[0])
