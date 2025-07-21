"""
Custom User Model for Videoflix Authentication
"""
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta


class CustomUserManager(UserManager):
    """Custom manager for CustomUser model"""
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)  # Superusers are always active
        extra_fields.setdefault('is_email_verified', True)  # Superusers don't need email verification

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    """
    email = models.EmailField(
        _('email address'), 
        unique=True,
        help_text=_('Required. Unique email address.')
    )
    is_email_verified = models.BooleanField(
        default=False,
        help_text=_('Designates whether the user has verified their email address.')
    )
    is_active = models.BooleanField(
        default=False,
        help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')
    )
    date_of_birth = models.DateField(
        null=True, 
        blank=True,
        help_text=_('User\'s date of birth (optional).')
    )

    # Use custom manager
    objects = CustomUserManager()
    profile_image = models.ImageField(
        upload_to='profile_images/',
        null=True,
        blank=True,
        help_text=_('User profile image (optional).')
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        db_table = 'auth_user_custom'
    
    def __str__(self):
        return f"{self.email} ({self.username})"
    
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()
    
    def get_short_name(self):
        """
        Return the short name for the user.
        """
        return self.first_name


class EmailVerificationToken(models.Model):
    """
    Model to store email verification tokens
    """
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='verification_token'
    )
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Email Verification Token')
        verbose_name_plural = _('Email Verification Tokens')
    
    def __str__(self):
        return f"Verification token for {self.user.email}"
    
    def is_expired(self):
        """
        Check if the token has expired (24 hours)
        """
        return timezone.now() > self.created_at + timedelta(hours=24)


class PasswordResetToken(models.Model):
    """
    Model to store password reset tokens
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reset_tokens'
    )
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = _('Password Reset Token')
        verbose_name_plural = _('Password Reset Tokens')
    
    def __str__(self):
        return f"Reset token for {self.user.email}"
