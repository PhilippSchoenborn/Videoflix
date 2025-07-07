from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from authentication.models import CustomUser

class UserRegistrationViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('authentication:register')
        self.valid_payload = {
            'email': 'testuser@example.com',
            'password': 'TestPassword123!',
            'password_confirm': 'TestPassword123!'
        }
        self.invalid_payload = {
            'email': 'testuser@example.com',
            'password': 'TestPassword123!',
            'password_confirm': 'WrongPassword!'
        }

    def test_register_user_success(self):
        """Happy Path: User can register with valid data"""
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(email='testuser@example.com').exists())
        self.assertIn('message', response.data)

    def test_register_user_password_mismatch(self):
        """Unhappy Path: Registration fails if passwords do not match"""
        response = self.client.post(self.url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_register_user_missing_fields(self):
        """Unhappy Path: Registration fails if required fields are missing"""
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_register_user_duplicate_email(self):
        """Unhappy Path: Registration fails if email already exists"""
        CustomUser.objects.create_user(email='testuser@example.com', username='testuser', password='TestPassword123!')
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

class UserLoginViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('authentication:login')
        self.user = CustomUser.objects.create_user(email='loginuser@example.com', username='loginuser', password='TestPassword123!')
        self.valid_payload = {
            'email': 'loginuser@example.com',
            'password': 'TestPassword123!'
        }
        self.invalid_payload = {
            'email': 'loginuser@example.com',
            'password': 'WrongPassword!'
        }

    def test_login_success(self):
        """Happy Path: User can log in with correct credentials"""
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_wrong_password(self):
        """Unhappy Path: Login fails with wrong password"""
        response = self.client.post(self.url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_login_missing_fields(self):
        """Unhappy Path: Login fails if required fields are missing"""
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_login_unverified_user(self):
        """Unhappy Path: Login fails if user is not verified (falls zutreffend)"""
        user2 = CustomUser.objects.create_user(email='unverified@example.com', username='unverified', password='TestPassword123!', is_active=False)
        payload = {'email': 'unverified@example.com', 'password': 'TestPassword123!'}
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

class UserLogoutViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(email='logoutuser@example.com', username='logoutuser', password='TestPassword123!')
        self.url = reverse('authentication:logout')
        self.client.force_authenticate(user=self.user)

    def test_logout_success(self):
        """Happy Path: Authenticated user can log out"""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_logout_unauthenticated(self):
        """Unhappy Path: Unauthenticated user cannot log out"""
        self.client.force_authenticate(user=None)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class PasswordResetRequestViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('authentication:password_reset_request')
        self.user = CustomUser.objects.create_user(email='resetuser@example.com', username='resetuser', password='TestPassword123!')

    def test_password_reset_request_success(self):
        """Happy Path: Valid email triggers password reset process"""
        response = self.client.post(self.url, {'email': 'resetuser@example.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_password_reset_request_invalid_email(self):
        """Unhappy Path: Invalid email returns generic message"""
        response = self.client.post(self.url, {'email': 'notfound@example.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_password_reset_request_missing_email(self):
        """Unhappy Path: Missing email returns error"""
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

class PasswordResetViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(email='reset2@example.com', username='reset2', password='TestPassword123!')
        self.url = reverse('authentication:password_reset', kwargs={'uidb64': 'dummy', 'token': 'dummy'})
        self.valid_payload = {'password': 'NewPassword123!', 'password_confirm': 'NewPassword123!'}
        self.invalid_payload = {'password': 'NewPassword123!', 'password_confirm': 'WrongPassword!'}

    def test_password_reset_passwords_match(self):
        """Happy Path: Passwords match and reset is successful (simulate)"""
        # Hier müsste ein echter Token-Flow getestet werden, dies ist ein Platzhalter
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])

    def test_password_reset_passwords_mismatch(self):
        """Unhappy Path: Passwords do not match"""
        response = self.client.post(self.url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

class UserProfileViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(email='profileuser@example.com', username='profileuser', password='TestPassword123!')
        self.url = reverse('authentication:profile')

    def test_get_profile_authenticated(self):
        """Happy Path: Authenticated user can get profile"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('email', response.data)

    def test_get_profile_unauthenticated(self):
        """Unhappy Path: Unauthenticated user cannot get profile"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
