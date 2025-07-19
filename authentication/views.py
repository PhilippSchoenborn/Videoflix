"""
Authentication views for user registration, login, logout, etc.
"""
import logging
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout, get_user_model
from django.shortcuts import get_object_or_404
from django_rq import get_queue

logger = logging.getLogger(__name__)

from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    PasswordResetRequestSerializer,
    PasswordResetSerializer,
    UserProfileSerializer
)
from .models import EmailVerificationToken, PasswordResetToken
from .utils import (
    create_verification_token,
    send_verification_email,
    create_password_reset_token,
    send_password_reset_email
)

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    """
    User registration endpoint
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        """
        Create user and handle validation errors
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            # Check for missing fields
            errors = serializer.errors
            if len(errors) > 1:
                return Response({
                    'error': 'Required fields are missing.'
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.save()
        
        # Create verification token and send email
        verification_token = create_verification_token(user)
        
        # Send verification email directly (will use appropriate backend)
        email_sent = send_verification_email(user, verification_token)
        
        if email_sent:
            logger.info(f"User {user.email} registered successfully, verification email sent")
            message = 'User created successfully. Please check your email to verify your account.'
        else:
            logger.warning(f"User {user.email} registered but verification email failed")
            message = 'User created successfully. However, there was an issue sending the verification email. Please contact support.'
        
        return Response({
            'message': message,
            'user': UserProfileSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class UserLoginView(generics.GenericAPIView):
    """
    User login endpoint
    """
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        """
        Authenticate user and return token
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            # Check for missing fields
            errors = serializer.errors
            if 'email' in errors and 'password' in errors:
                return Response({
                    'error': 'Both email and password are required.'
                }, status=status.HTTP_400_BAD_REQUEST)
            elif 'email' in errors:
                return Response({
                    'error': 'Email is required.'
                }, status=status.HTTP_400_BAD_REQUEST)
            elif 'password' in errors:
                return Response({
                    'error': 'Password is required.'
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': UserProfileSerializer(user).data
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def user_logout_view(request):
    """
    User logout endpoint
    """
    try:
        # Delete the user's token
        request.user.auth_token.delete()
        logout(request)
        return Response(
            {'message': 'Successfully logged out'},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {'error': 'Logout failed'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def verify_email_view(request, uidb64, token):
    """
    Email verification endpoint with uidb64 and token
    """
    try:
        verification_token = EmailVerificationToken.objects.get(token=token)
        user = verification_token.user
        user.is_email_verified = True
        user.is_active = True
        user.save()
        verification_token.delete()
        return Response(
            {'message': 'Email verified successfully'},
            status=status.HTTP_200_OK
        )
    except EmailVerificationToken.DoesNotExist:
        return Response(
            {'error': 'Invalid verification token'},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def verify_email_token_view(request, token):
    """
    Email verification endpoint with automatic redirect to frontend login
    """
    from django.shortcuts import redirect
    from django.conf import settings
    
    try:
        verification_token = EmailVerificationToken.objects.get(token=token)
        
        if verification_token.is_expired():
            # Redirect to frontend with error
            frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:5173')
            return redirect(f"{frontend_url}/login?verification=expired")
        
        user = verification_token.user
        
        # Activate user and verify email
        user.is_active = True
        if hasattr(user, 'is_email_verified'):
            user.is_email_verified = True
        user.save()
        
        # Remove verification token
        verification_token.delete()
        
        logger.info(f"✅ User {user.email} verified successfully via web interface (is_active={user.is_active}, is_email_verified={getattr(user, 'is_email_verified', None)})")
        
        # Redirect to frontend login page with success message
        frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:5173')
        return redirect(f"{frontend_url}/login?verification=success&email={user.email}")
        
    except EmailVerificationToken.DoesNotExist:
        # Redirect to frontend with error
        frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:5173')
        return redirect(f"{frontend_url}/login?verification=invalid")


class PasswordResetRequestView(generics.GenericAPIView):
    """
    Password reset request endpoint
    """
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        """
        Send password reset email if user exists
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'error': 'Email is required.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(email=email)
            reset_token = create_password_reset_token(user)
            
            # Send reset email directly (will use appropriate backend)
            email_sent = send_password_reset_email(user, reset_token)
            
            if email_sent:
                logger.info(f"Password reset email sent successfully to {user.email}")
            else:
                logger.warning(f"Failed to send password reset email to {user.email}")
                
        except User.DoesNotExist:
            pass  # Don't reveal if email exists
        
        return Response(
            {'message': 'If the email exists, a reset link has been sent'},
            status=status.HTTP_200_OK
        )


class PasswordResetView(generics.GenericAPIView):
    """
    Password reset endpoint
    """
    serializer_class = PasswordResetSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        """
        Reset user password with token
        """
        # Token aus URL nehmen wenn vorhanden, sonst aus Body
        url_token = kwargs.get('token')
        
        if url_token:
            # Token aus URL verwenden
            token = url_token
            # Nur Password aus Body validieren
            password = request.data.get('password')
            if not password:
                return Response({
                    'error': 'Password is required.'
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Fallback: Token und Password aus Body
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                errors = serializer.errors
                if 'token' in errors and 'password' in errors:
                    return Response({
                        'error': 'Both token and password are required.'
                    }, status=status.HTTP_400_BAD_REQUEST)
                elif 'token' in errors:
                    return Response({
                        'error': 'Token is required.'
                    }, status=status.HTTP_400_BAD_REQUEST)
                elif 'password' in errors:
                    return Response({
                        'error': 'Password is required.'
                    }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            
            token = serializer.validated_data['token']
            password = serializer.validated_data['password']
        
        try:
            reset_token = PasswordResetToken.objects.get(
                token=token,
                used=False
            )
            
            # Check if token is not expired (24 hours)
            from datetime import timedelta
            from django.utils import timezone
            
            if reset_token.created_at < timezone.now() - timedelta(hours=24):
                return Response(
                    {'error': 'Reset token has expired'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Reset password
            user = reset_token.user
            user.set_password(password)
            user.save()
            
            # Token bleibt wiederverwendbar für Testing/Development
            # reset_token.used = True  # Kommentiert aus für mehrfache Nutzung
            # reset_token.save()
            
            return Response(
                {'message': 'Password reset successfully'},
                status=status.HTTP_200_OK
            )
        
        except PasswordResetToken.DoesNotExist:
            return Response(
                {'error': 'Invalid reset token'},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    User profile view
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """
        Return the current user
        """
        return self.request.user


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def check_email_exists(request):
    """
    Check if email exists in the system
    """
    email = request.data.get('email')
    if not email:
        return Response(
            {'error': 'Email is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user_exists = User.objects.filter(email__iexact=email).exists()
        return Response({
            'exists': user_exists,
            'email': email
        }, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error checking email existence: {str(e)}")
        return Response(
            {'error': 'An error occurred while checking email'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
