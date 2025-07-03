"""
Utility functions for authentication app
"""
import secrets
import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model
from .models import EmailVerificationToken, PasswordResetToken

User = get_user_model()


def generate_verification_token():
    """
    Generate a unique verification token
    """
    return secrets.token_urlsafe(32)


def create_verification_token(user):
    """
    Create email verification token for user
    """
    token = generate_verification_token()
    EmailVerificationToken.objects.update_or_create(
        user=user,
        defaults={'token': token}
    )
    return token


def send_verification_email(user, verification_token):
    """
    Send email verification email to user
    """
    subject = 'Verify your Videoflix account'
    verification_link = f"{settings.FRONTEND_URL}/verify-email/{verification_token}"
    
    html_message = render_to_string('authentication/emails/verification_email.html', {
        'user': user,
        'verification_link': verification_link,
    })
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )


def create_password_reset_token(user):
    """
    Create password reset token for user
    """
    token = generate_verification_token()
    PasswordResetToken.objects.create(
        user=user,
        token=token
    )
    return token


def send_password_reset_email(user, reset_token):
    """
    Send password reset email to user
    """
    subject = 'Reset your Videoflix password'
    reset_link = f"{settings.FRONTEND_URL}/reset-password/{reset_token}"
    
    html_message = render_to_string('authentication/emails/password_reset_email.html', {
        'user': user,
        'reset_link': reset_link,
    })
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )


def validate_password_strength(password):
    """
    Validate password strength
    Returns tuple (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one digit."
    
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter."
    
    if not any(char.islower() for char in password):
        return False, "Password must contain at least one lowercase letter."
    
    return True, ""


def clean_expired_tokens():
    """
    Clean up expired tokens (background task)
    """
    from datetime import timedelta
    from django.utils import timezone
    
    expiry_time = timezone.now() - timedelta(hours=24)
    
    # Delete expired verification tokens
    EmailVerificationToken.objects.filter(
        created_at__lt=expiry_time
    ).delete()
    
    # Delete expired reset tokens
    PasswordResetToken.objects.filter(
        created_at__lt=expiry_time
    ).delete()
