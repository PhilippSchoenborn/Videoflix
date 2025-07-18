"""
Serializers for authentication app
"""
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from .utils import validate_password_strength
from django.conf import settings

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    """
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = (
            'email', 
            'username', 
            'first_name', 
            'last_name', 
            'password', 
            'password_confirm'
        )
    
    def validate_email(self, value):
        """
        Validate email uniqueness
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError({
                'error': 'A user with this email already exists.'
            })
        return value

    def validate(self, attrs):
        """
        Validate password confirmation and strength
        """
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError({
                'error': 'Passwords do not match.'
            })
        # Validate password strength
        is_valid, error_message = validate_password_strength(password)
        if not is_valid:
            raise serializers.ValidationError({
                'error': error_message
            })
        return attrs
    
    def create(self, validated_data):
        """
        Create user with validated data
        """
        import logging
        logger = logging.getLogger(__name__)
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        logger.info(f"User created: {user.email} (default is_active={user.is_active}, is_email_verified={getattr(user, 'is_email_verified', None)})")
        
        # Always create user as inactive and unverified (for email verification)
        user.is_active = False
        if hasattr(user, 'is_email_verified'):
            user.is_email_verified = False
        logger.info(f"User set inactive/unverified: is_active={user.is_active}, is_email_verified={getattr(user, 'is_email_verified', None)}")
        user.save()
        logger.info(f"User saved: {user.email} (is_active={user.is_active}, is_email_verified={getattr(user, 'is_email_verified', None)})")
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs):
        """
        Validate user credentials
        """
        email = attrs.get('email')
        password = attrs.get('password')
        import logging
        logger = logging.getLogger(__name__)
        logger.debug(f"Login attempt: email={email}")
        BYPASS_EMAIL_VERIFICATION = getattr(settings, 'BYPASS_EMAIL_VERIFICATION', False)
        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )
            if not user:
                logger.warning(f"Login failed for email: {email} (user not found or wrong password)")
                raise serializers.ValidationError({
                    'error': 'Invalid email or password.'
                })
            if not user.is_email_verified and not BYPASS_EMAIL_VERIFICATION:
                logger.warning(f"Login failed for email: {email} (email not verified)")
                raise serializers.ValidationError({
                    'error': 'Please verify your email before logging in.'
                })
            logger.info(f"Login successful for email: {email}")
            attrs['user'] = user
            return attrs
        logger.warning(f"Login failed: missing email or password (email={email})")
        raise serializers.ValidationError({
            'error': 'Both email and password are required.'
        })


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for password reset request
    """
    email = serializers.EmailField()


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for password reset
    """
    token = serializers.CharField()
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs):
        """
        Validate password confirmation and strength
        """
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        
        if password != password_confirm:
            raise serializers.ValidationError({
                'error': 'Password confirmation does not match.'
            })
        
        # Validate password strength
        is_valid, error_message = validate_password_strength(password)
        if not is_valid:
            raise serializers.ValidationError({
                'error': error_message
            })
        
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile
    """
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'date_of_birth',
            'profile_image',
            'is_email_verified',
            'date_joined'
        )
        read_only_fields = ('id', 'email', 'is_email_verified', 'date_joined')
