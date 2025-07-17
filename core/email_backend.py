"""
Custom Email Backend for Development
Saves emails to files AND outputs to console
"""
import os
import time
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.backends.filebased import EmailBackend as FileBasedEmailBackend
from django.core.mail.backends.console import EmailBackend as ConsoleEmailBackend
from django.conf import settings


class DevelopmentEmailBackend(BaseEmailBackend):
    """
    Email backend that saves emails to files AND outputs to console
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize both backends
        self.file_backend = FileBasedEmailBackend(*args, **kwargs)
        self.console_backend = ConsoleEmailBackend(*args, **kwargs)
        
        # Ensure email directory exists
        email_dir = getattr(settings, 'EMAIL_FILE_PATH', os.path.join(settings.BASE_DIR, 'logs', 'emails'))
        os.makedirs(email_dir, exist_ok=True)
    
    def send_messages(self, email_messages):
        """
        Send messages using both file and console backends
        """
        if not email_messages:
            return 0
        
        # Send to file backend (saves to logs/emails/)
        file_count = self.file_backend.send_messages(email_messages)
        
        # Send to console backend (prints to terminal)
        console_count = self.console_backend.send_messages(email_messages)
        
        # Add custom logging for verification emails
        for message in email_messages:
            if 'verification' in message.subject.lower() or 'verify' in message.subject.lower():
                self._log_verification_email(message)
        
        return max(file_count, console_count)
    
    def _log_verification_email(self, message):
        """
        Log verification email details
        """
        print("\n" + "="*60)
        print("📧 EMAIL VERIFICATION SENT")
        print("="*60)
        print(f"To: {', '.join(message.to)}")
        print(f"Subject: {message.subject}")
        
        # Extract verification link from body
        body = message.body
        if 'verify-email' in body:
            lines = body.split('\n')
            for line in lines:
                if 'verify-email' in line and 'http' in line:
                    print(f"🔗 Verification Link: {line.strip()}")
                    break
        
        print(f"💾 Email saved to: logs/emails/")
        print("="*60)
        print("💡 Use: python manage.py verify_email --list-emails")
        print("💡 Use: python manage.py verify_email --list-tokens")
        print("="*60 + "\n")
