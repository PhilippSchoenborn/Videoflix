from django.core.management.base import BaseCommand
from authentication.models import CustomUser, EmailVerificationToken
from django.utils import timezone

class Command(BaseCommand):
    help = 'Manually verify a user by email'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email address of the user to verify')

    def handle(self, *args, **options):
        email = options['email']
        
        try:
            user = CustomUser.objects.get(email=email)
            
            # Set user as active and email verified
            user.is_active = True
            user.is_email_verified = True
            user.save()
            
            # Delete verification tokens
            EmailVerificationToken.objects.filter(user=user).delete()
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ User {email} successfully verified!')
            )
            self.stdout.write(f'is_active: {user.is_active}')
            self.stdout.write(f'is_email_verified: {user.is_email_verified}')
            
        except CustomUser.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'❌ User with email {email} does not exist')
            )
