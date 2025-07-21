"""
Django signals for authentication app
"""
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser, EmailVerificationToken, PasswordResetToken
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


@receiver(post_save, sender=CustomUser)
def create_user_profile_actions(sender, instance, created, **kwargs):
    """
    Signal triggered when a new user is created
    """
    if created:
        logger.info(f'New user created: {instance.email} (ID: {instance.id})')
        
        # Skip email verification for superusers (admin users)
        if instance.is_superuser:
            logger.info(f'Skipping email verification for superuser: {instance.email}')
            return
            
        # Entferne automatische Verifizierung im DEBUG
        # Nur Token erzeugen, keine automatische Verifizierung
        try:
            EmailVerificationToken.objects.filter(user=instance).delete()
            from .utils import generate_verification_token
            token = generate_verification_token()
            verification_token = EmailVerificationToken.objects.create(user=instance, token=token)
            logger.info(f'Email verification token created for user {instance.email}')
        except Exception as e:
            logger.error(f'Error creating verification token for user {instance.email}: {str(e)}')


@receiver(post_save, sender=CustomUser)
def user_profile_updated(sender, instance, created, **kwargs):
    """
    Signal triggered when user profile is updated
    """
    if not created:
        logger.info(f'User profile updated: {instance.email} (ID: {instance.id})')
        
        # Log important profile changes
        if instance.is_email_verified and hasattr(instance, '_email_just_verified'):
            logger.info(f'Email verified for user: {instance.email}')
            
        if instance.is_active and hasattr(instance, '_account_just_activated'):
            logger.info(f'Account activated for user: {instance.email}')


@receiver(post_save, sender=EmailVerificationToken)
def email_verification_token_created(sender, instance, created, **kwargs):
    """
    Signal triggered when email verification token is created
    """
    if created:
        logger.info(f'Email verification token created for user: {instance.user.email}')
        
        # In production, send verification email via background task
        if settings.DEBUG:
            print(f'Verification email would be sent to {instance.user.email} with token: {instance.token}')


@receiver(post_save, sender=PasswordResetToken)
def password_reset_token_created(sender, instance, created, **kwargs):
    """
    Signal triggered when password reset token is created
    """
    if created:
        logger.info(f'Password reset token created for user: {instance.user.email}')
        
        # In production, send password reset email via background task
        if settings.DEBUG:
            print(f'Password reset email would be sent to {instance.user.email} with token: {instance.token}')


@receiver(pre_delete, sender=CustomUser)
def user_deletion_cleanup(sender, instance, **kwargs):
    """
    Signal triggered before user deletion
    Clean up related data and log the action
    """
    logger.warning(f'User deletion initiated: {instance.email} (ID: {instance.id})')
    
    # Clean up related tokens
    EmailVerificationToken.objects.filter(user=instance).delete()
    PasswordResetToken.objects.filter(user=instance).delete()
    
    # Log for audit purposes
    logger.info(f'Cleaned up tokens for deleted user: {instance.email}')
