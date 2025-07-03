"""
Serializers for authentication app
"""
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from .utils import validate_password_strength

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
            raise serializers.ValidationError(
                "Please check your inputs and try again."
            )
        return value
    
    def validate(self, attrs):
        """
        Validate password confirmation and strength
        """
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        
        if password != password_confirm:
            raise serializers.ValidationError(
                "Please check your inputs and try again."
            )
        
        # Validate password strength
        is_valid, error_message = validate_password_strength(password)
        if not is_valid:
            raise serializers.ValidationError(error_message)
        
        return attrs
    
    def create(self, validated_data):
        """
        Create user with validated data
        """
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
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
        
        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )
            
            if not user:
                raise serializers.ValidationError(
                    "Please check your inputs and try again."
                )
            
            if not user.is_email_verified:
                raise serializers.ValidationError(
                    "Please verify your email before logging in."
                )
            
            attrs['user'] = user
            return attrs
        
        raise serializers.ValidationError(
            "Please check your inputs and try again."
        )


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
            raise serializers.ValidationError(
                "Password confirmation does not match."
            )
        
        # Validate password strength
        is_valid, error_message = validate_password_strength(password)
        if not is_valid:
            raise serializers.ValidationError(error_message)
        
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
