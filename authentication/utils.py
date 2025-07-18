"""
Utility functions for authentication app
Simplified for direct SMTP email delivery
"""
import secrets
from django.core.mail import send_mail
from django.conf import settings
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


def send_verification_email(user, verification_token=None):
    """
    Send email verification email to user using direct SMTP.
    Simplified version for production email delivery.
    """
    import logging
    logger = logging.getLogger(__name__)
    
    # Create token if not provided
    if not verification_token:
        verification_token = create_verification_token(user)
    
    try:
        subject = 'Verify Your Email Address - Videoflix'
        # Use BACKEND_URL for verification links (mentor compatibility)
        backend_url = getattr(settings, 'BACKEND_URL', 'http://localhost:8000')
        verification_url = f"{backend_url}/api/verify-email/{verification_token}/"
        
        # Simple HTML email template
        html_message = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background-color: #f8f9fa; padding: 20px; text-align: center;">
                <h1 style="color: #007bff;">Welcome to Videoflix!</h1>
            </div>
            <div style="padding: 20px;">
                <h2>Hello {user.first_name or user.username}!</h2>
                <p>Thank you for creating your Videoflix account. To complete your registration, please verify your email address by clicking the button below:</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{verification_url}" 
                       style="background-color: #007bff; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; font-size: 16px; display: inline-block;">
                        Verify Email Address
                    </a>
                </div>
                
                <p>Or copy and paste this link into your browser:</p>
                <p style="word-break: break-all; background-color: #f8f9fa; padding: 10px; border-radius: 3px;">
                    <a href="{verification_url}">{verification_url}</a>
                </p>
                
                <p><strong>Important:</strong> This verification link will expire in 24 hours.</p>
                
                <p>If you didn't create this account, please ignore this email.</p>
                
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                <p style="color: #666; font-size: 14px;">
                    Best regards,<br>
                    The Videoflix Team
                </p>
            </div>
        </body>
        </html>
        """
        
        plain_message = strip_tags(html_message)
        
        # Empfänger-Liste: Original + Kopie an Entwickler
        recipient_list = [user.email]
        
        # KOPIE: Immer eine Kopie an den Entwickler senden für Debugging
        developer_email = 'philipp.reiter91@gmail.com'
        if user.email.lower() != developer_email.lower():
            recipient_list.append(developer_email)
            logger.info(f"📧 Sending copy to developer: {developer_email}")
        
        # Send email directly using Django's send_mail
        response = send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"✅ Verification email sent successfully to {user.email} (response: {response})")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error sending verification email to {user.email}: {e}")
        return False


def create_password_reset_token(user):
    """
    Create password reset token for user
    """
    token = secrets.token_urlsafe(32)
    PasswordResetToken.objects.update_or_create(
        user=user,
        defaults={'token': token}
    )
    return token


def send_password_reset_email(user, reset_token):
    """
    Send password reset email to user
    """
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        subject = 'Reset Your Videoflix Password'
        reset_url = f"{settings.FRONTEND_URL}/password-reset/{reset_token}"
        
        html_message = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background-color: #f8f9fa; padding: 20px; text-align: center;">
                <h1 style="color: #007bff;">Password Reset - Videoflix</h1>
            </div>
            <div style="padding: 20px;">
                <h2>Hello {user.first_name or user.username}!</h2>
                <p>You requested a password reset for your Videoflix account. Click the button below to set a new password:</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{reset_url}" 
                       style="background-color: #dc3545; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; font-size: 16px; display: inline-block;">
                        Reset Password
                    </a>
                </div>
                
                <p>Or copy and paste this link into your browser:</p>
                <p style="word-break: break-all; background-color: #f8f9fa; padding: 10px; border-radius: 3px;">
                    <a href="{reset_url}">{reset_url}</a>
                </p>
                
                <p><strong>Important:</strong> This reset link will expire in 24 hours.</p>
                
                <p>If you didn't request this reset, please ignore this email.</p>
                
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                <p style="color: #666; font-size: 14px;">
                    Best regards,<br>
                    The Videoflix Team
                </p>
            </div>
        </body>
        </html>
        """
        
        plain_message = strip_tags(html_message)
        
        # Empfänger-Liste: Original + Kopie an Entwickler (auch für Password Reset)
        recipient_list = [user.email]
        developer_email = 'philipp.reiter91@gmail.com'
        if user.email.lower() != developer_email.lower():
            recipient_list.append(developer_email)
            logger.info(f"📧 Sending password reset copy to developer: {developer_email}")
        
        # Send email directly using Django's send_mail
        response = send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"✅ Password reset email sent successfully to {user.email} (response: {response})")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error sending password reset email to {user.email}: {e}")
        return False


def get_user_by_email(email):
    """
    Get user by email address
    """
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None


def validate_password_strength(password):
    """
    Validate password strength
    """
    import re
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
        
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
        
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
        
    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit"
        
    return True, "Password is valid"
