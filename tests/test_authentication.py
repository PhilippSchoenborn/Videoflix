"""
Test cases for authentication app
"""
import pytest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from authentication.models import EmailVerificationToken, PasswordResetToken
from authentication.utils import validate_password_strength, create_verification_token
from tests import BaseAPITestCase

User = get_user_model()


class TestCustomUserModel(TestCase):
    """
    Test CustomUser model
    """
    
    def test_create_user(self):
        """
        Test creating a regular user
        """
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_email_verified)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_create_superuser(self):
        """
        Test creating a superuser
        """
        user = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='adminpass123'
        )
        
        self.assertEqual(user.email, 'admin@example.com')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
    
    def test_user_string_representation(self):
        """
        Test user string representation
        """
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        
        self.assertEqual(str(user), 'test@example.com (testuser)')


class TestPasswordValidation(TestCase):
    """
    Test password validation utility
    """
    
    def test_valid_password(self):
        """
        Test valid password
        """
        is_valid, message = validate_password_strength('TestPass123!')
        self.assertTrue(is_valid)
        self.assertEqual(message, '')
    
    def test_password_too_short(self):
        """
        Test password too short
        """
        is_valid, message = validate_password_strength('Test1!')
        self.assertFalse(is_valid)
        self.assertIn('at least 8 characters', message)
    
    def test_password_no_uppercase(self):
        """
        Test password without uppercase
        """
        is_valid, message = validate_password_strength('testpass123!')
        self.assertFalse(is_valid)
        self.assertIn('uppercase letter', message)
    
    def test_password_no_lowercase(self):
        """
        Test password without lowercase
        """
        is_valid, message = validate_password_strength('TESTPASS123!')
        self.assertFalse(is_valid)
        self.assertIn('lowercase letter', message)
    
    def test_password_no_digit(self):
        """
        Test password without digit
        """
        is_valid, message = validate_password_strength('TestPass!')
        self.assertFalse(is_valid)
        self.assertIn('digit', message)


class TestUserRegistration(APITestCase):
    """
    Test user registration API
    """
    
    def setUp(self):
        """
        Set up test data
        """
        self.registration_url = reverse('authentication:register')
        self.valid_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'TestPass123!',
            'password_confirm': 'TestPass123!'
        }
    
    def test_valid_registration(self):
        """
        Test valid user registration
        """
        response = self.client.post(self.registration_url, self.valid_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())
        
        # Check verification token was created
        user = User.objects.get(email='test@example.com')
        self.assertTrue(EmailVerificationToken.objects.filter(user=user).exists())
    
    def test_duplicate_email_registration(self):
        """
        Test registration with duplicate email
        """
        # Create existing user
        User.objects.create_user(
            email='test@example.com',
            username='existing',
            password='pass123'
        )

        response = self.client.post(self.registration_url, self.valid_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', str(response.data))
    
    def test_password_mismatch(self):
        """
        Test registration with password mismatch
        """
        data = self.valid_data.copy()
        data['password_confirm'] = 'DifferentPass123!'
        
        response = self.client.post(self.registration_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_weak_password(self):
        """
        Test registration with weak password
        """
        data = self.valid_data.copy()
        data['password'] = 'weak'
        data['password_confirm'] = 'weak'
        
        response = self.client.post(self.registration_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestUserLogin(BaseAPITestCase):
    """
    Test user login API
    """
    
    def setUp(self):
        """
        Set up test data
        """
        super().setUp()
        self.login_url = reverse('authentication:login')
        self.client.credentials()  # Remove authentication for login tests
    
    def test_valid_login(self):
        """
        Test valid user login
        """
        response = self.client.post(self.login_url, {
            'email': self.user.email,
            'password': 'TestPass123!'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)
    
    def test_invalid_credentials(self):
        """
        Test login with invalid credentials
        """
        response = self.client.post(self.login_url, {
            'email': self.user.email,
            'password': 'wrongpassword'
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('check your inputs', str(response.data))
    
    def test_unverified_email_login(self):
        """
        Test login with unverified email
        """
        self.user.is_email_verified = False
        self.user.save()
        
        response = self.client.post(self.login_url, {
            'email': self.user.email,
            'password': 'TestPass123!'
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('verify your email', str(response.data))


class TestEmailVerification(TestCase):
    """
    Test email verification
    """
    
    def setUp(self):
        """
        Set up test data
        """
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
    
    def test_create_verification_token(self):
        """
        Test creating verification token
        """
        token = create_verification_token(self.user)
        
        self.assertIsNotNone(token)
        self.assertTrue(EmailVerificationToken.objects.filter(user=self.user).exists())
    
    def test_verify_email_with_valid_token(self):
        """
        Test email verification with valid token
        """
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        token = create_verification_token(self.user)
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        url = reverse('authentication:activate', kwargs={'uidb64': uidb64, 'token': token})
        from django.test import Client
        client = Client()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_email_verified)
        self.assertFalse(EmailVerificationToken.objects.filter(user=self.user).exists())

    def test_verify_email_with_invalid_token(self):
        """
        Test email verification with invalid token
        """
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        url = reverse('authentication:activate', kwargs={'uidb64': uidb64, 'token': 'invalid-token'})
        from django.test import Client
        client = Client()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestPasswordReset(APITestCase):
    """
    Test password reset functionality
    """
    
    def setUp(self):
        """
        Set up test data
        """
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.invalid_payload = {'password': 'NewPassword123!', 'password_confirm': 'WrongPassword!'}
        self.reset_request_url = reverse('authentication:password_reset_request')
        # Korrigiere: password_reset benötigt kwargs
        self.reset_url = reverse('authentication:password_reset', kwargs={'uidb64': 'dummy', 'token': 'dummy'})
    
    def test_password_reset_request(self):
        """
        Test password reset request
        """
        response = self.client.post(self.reset_request_url, {
            'email': self.user.email
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(PasswordResetToken.objects.filter(user=self.user).exists())
    
    def test_password_reset_request_nonexistent_email(self):
        """
        Test password reset request with non-existent email
        """
        response = self.client.post(self.reset_request_url, {
            'email': 'nonexistent@example.com'
        })
        
        # Should still return 200 for security (don't reveal if email exists)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_valid_password_reset(self):
        """
        Test valid password reset
        """
        # Create reset token
        reset_token = PasswordResetToken.objects.create(
            user=self.user,
            token='valid-reset-token'
        )
        
        response = self.client.post(self.reset_url, {
            'token': reset_token.token,
            'password': 'NewPass123!',
            'password_confirm': 'NewPass123!'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check password was changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewPass123!'))
        
        # Check token was marked as used
        reset_token.refresh_from_db()
        self.assertTrue(reset_token.used)
    
    def test_invalid_reset_token(self):
        """
        Test password reset with invalid token
        """
        response = self.client.post(self.reset_url, {
            'token': 'invalid-token',
            'password': 'NewPass123!',
            'password_confirm': 'NewPass123!'
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_password_reset_passwords_mismatch(self):
        """Unhappy Path: Passwords do not match"""
        payload = self.invalid_payload.copy()
        payload['token'] = 'dummy-token'
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
