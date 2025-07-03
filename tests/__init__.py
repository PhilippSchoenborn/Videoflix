"""
Base test configurations and utilities
"""
import os
import django
from django.conf import settings

# Configure Django settings before importing anything else
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()

import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

User = get_user_model()


@pytest.fixture
def user_data():
    """
    Fixture for user data
    """
    return {
        'email': 'test@example.com',
        'username': 'testuser',
        'password': 'TestPass123!',
        'first_name': 'Test',
        'last_name': 'User'
    }


@pytest.fixture
def create_user(user_data):
    """
    Fixture to create a test user
    """
    def _create_user(**kwargs):
        data = user_data.copy()
        data.update(kwargs)
        user = User.objects.create_user(**data)
        user.is_email_verified = True
        user.save()
        return user
    return _create_user


@pytest.fixture
def authenticated_client(create_user):
    """
    Fixture for authenticated API client
    """
    from rest_framework.test import APIClient
    
    user = create_user()
    token, created = Token.objects.get_or_create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    return client, user


class BaseTestCase(TestCase):
    """
    Base test case with common setup
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
    
    def create_user(self, **kwargs):
        """
        Helper method to create a test user
        """
        data = self.user_data.copy()
        data.update(kwargs)
        user = User.objects.create_user(**data)
        user.is_email_verified = True
        user.save()
        return user


class BaseAPITestCase(APITestCase):
    """
    Base API test case with authentication
    """
    
    def setUp(self):
        """
        Set up test data and authentication
        """
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'TestPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        self.user = self.create_user()
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
    
    def create_user(self, **kwargs):
        """
        Helper method to create a test user
        """
        data = self.user_data.copy()
        data.update(kwargs)
        user = User.objects.create_user(**data)
        user.is_email_verified = True
        user.save()
        return user
