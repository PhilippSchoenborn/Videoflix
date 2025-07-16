"""
Authentication views for user registration, login, logout, etc.
"""
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout, get_user_model
from django.shortcuts import get_object_or_404
from django_rq import get_queue

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
    
    def perform_create(self, serializer):
        """
        Create user and send verification email
        """
        user = serializer.save()
        
        # Create verification token
        verification_token = create_verification_token(user)
        
        # Send verification email asynchronously
        queue = get_queue('default')
        queue.enqueue(
            send_verification_email,
            user,
            verification_token
        )
        
        return user


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
        serializer.is_valid(raise_exception=True)
        
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
    Email verification endpoint
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
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(email=email)
            reset_token = create_password_reset_token(user)
            
            # Send reset email asynchronously
            queue = get_queue('default')
            queue.enqueue(
                send_password_reset_email,
                user,
                reset_token
            )
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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
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
            
            # Mark token as used
            reset_token.used = True
            reset_token.save()
            
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
