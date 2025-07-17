"""
Django management command for email verification management
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from authentication.models import EmailVerificationToken
from django.utils import timezone
from django.conf import settings
import os
import glob
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

User = get_user_model()


class Command(BaseCommand):
    help = 'Manage email verification - list tokens, verify users, and view email files'

    def add_arguments(self, parser):
        parser.add_argument(
            '--list-tokens',
            action='store_true',
            help='List all active verification tokens'
        )
        parser.add_argument(
            '--verify',
            type=str,
            help='Verify user by email address'
        )
        parser.add_argument(
            '--verify-token',
            type=str,
            help='Verify user by token'
        )
        parser.add_argument(
            '--list-emails',
            action='store_true',
            help='List all email files in the project'
        )
        parser.add_argument(
            '--show-email',
            type=str,
            help='Show content of specific email file'
        )
        parser.add_argument(
            '--cleanup',
            action='store_true',
            help='Remove expired tokens and old email files'
        )

    def handle(self, *args, **options):
        if options['list_tokens']:
            self.list_tokens()
        elif options['verify']:
            self.verify_user_by_email(options['verify'])
        elif options['verify_token']:
            self.verify_user_by_token(options['verify_token'])
        elif options['list_emails']:
            self.list_email_files()
        elif options['show_email']:
            self.show_email_content(options['show_email'])
        elif options['cleanup']:
            self.cleanup_old_data()
        else:
            self.show_help()

    def show_help(self):
        """Display help information"""
        self.stdout.write(f"\n{Fore.CYAN}📧 EMAIL VERIFICATION MANAGEMENT{Style.RESET_ALL}")
        self.stdout.write(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        self.stdout.write(f"\n{Fore.YELLOW}Available commands:{Style.RESET_ALL}")
        self.stdout.write(f"  {Fore.GREEN}--list-tokens{Style.RESET_ALL}     : List all active verification tokens")
        self.stdout.write(f"  {Fore.GREEN}--verify EMAIL{Style.RESET_ALL}    : Verify user by email address")
        self.stdout.write(f"  {Fore.GREEN}--verify-token TOKEN{Style.RESET_ALL} : Verify user by token")
        self.stdout.write(f"  {Fore.GREEN}--list-emails{Style.RESET_ALL}     : List all email files")
        self.stdout.write(f"  {Fore.GREEN}--show-email FILE{Style.RESET_ALL} : Show email file content")
        self.stdout.write(f"  {Fore.GREEN}--cleanup{Style.RESET_ALL}         : Remove expired tokens and old emails")
        self.stdout.write(f"\n{Fore.YELLOW}Examples:{Style.RESET_ALL}")
        self.stdout.write(f"  python manage.py verify_email --list-tokens")
        self.stdout.write(f"  python manage.py verify_email --verify user@example.com")
        self.stdout.write(f"  python manage.py verify_email --verify-token abc123def456")
        self.stdout.write(f"  python manage.py verify_email --list-emails")
        self.stdout.write("")

    def list_tokens(self):
        """List all active verification tokens"""
        tokens = EmailVerificationToken.objects.all().order_by('-created_at')
        
        if not tokens.exists():
            self.stdout.write(f"{Fore.YELLOW}No verification tokens found.{Style.RESET_ALL}")
            return

        self.stdout.write(f"\n{Fore.CYAN}📧 ACTIVE VERIFICATION TOKENS{Style.RESET_ALL}")
        self.stdout.write(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        for token in tokens:
            status = f"{Fore.GREEN}✅ VERIFIED" if token.user.is_active else f"{Fore.RED}❌ PENDING"
            expired = f"{Fore.RED}(EXPIRED)" if token.is_expired() else f"{Fore.GREEN}(VALID)"
            
            self.stdout.write(f"\n{Fore.YELLOW}Email:{Style.RESET_ALL} {token.user.email}")
            self.stdout.write(f"{Fore.YELLOW}Token:{Style.RESET_ALL} {token.token}")
            self.stdout.write(f"{Fore.YELLOW}Status:{Style.RESET_ALL} {status}{Style.RESET_ALL}")
            self.stdout.write(f"{Fore.YELLOW}Expires:{Style.RESET_ALL} {expired}{Style.RESET_ALL}")
            self.stdout.write(f"{Fore.YELLOW}Created:{Style.RESET_ALL} {token.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            self.stdout.write(f"{Fore.BLUE}Verification URL:{Style.RESET_ALL} {settings.FRONTEND_URL}/verify-email/{token.token}")
            self.stdout.write(f"{Fore.CYAN}{'-'*60}{Style.RESET_ALL}")

    def verify_user_by_email(self, email):
        """Verify user by email address"""
        try:
            user = User.objects.get(email=email)
            
            if user.is_active:
                self.stdout.write(f"{Fore.GREEN}✅ User {email} is already verified!{Style.RESET_ALL}")
                return
            
            # Activate user
            user.is_active = True
            user.save()
            
            # Remove verification token
            EmailVerificationToken.objects.filter(user=user).delete()
            
            self.stdout.write(f"{Fore.GREEN}✅ Successfully verified user: {email}{Style.RESET_ALL}")
            self.stdout.write(f"{Fore.YELLOW}📧 Verification tokens removed.{Style.RESET_ALL}")
            
        except User.DoesNotExist:
            self.stdout.write(f"{Fore.RED}❌ User with email {email} not found.{Style.RESET_ALL}")

    def verify_user_by_token(self, token):
        """Verify user by token"""
        try:
            verification_token = EmailVerificationToken.objects.get(token=token)
            
            if verification_token.is_expired():
                self.stdout.write(f"{Fore.RED}❌ Token has expired.{Style.RESET_ALL}")
                return
            
            user = verification_token.user
            
            if user.is_active:
                self.stdout.write(f"{Fore.GREEN}✅ User {user.email} is already verified!{Style.RESET_ALL}")
                return
            
            # Activate user
            user.is_active = True
            user.save()
            
            # Remove verification token
            verification_token.delete()
            
            self.stdout.write(f"{Fore.GREEN}✅ Successfully verified user: {user.email}{Style.RESET_ALL}")
            self.stdout.write(f"{Fore.YELLOW}📧 Verification token removed.{Style.RESET_ALL}")
            
        except EmailVerificationToken.DoesNotExist:
            self.stdout.write(f"{Fore.RED}❌ Invalid verification token.{Style.RESET_ALL}")

    def list_email_files(self):
        """List all email files in the project"""
        email_dir = os.path.join(settings.BASE_DIR, 'logs', 'emails')
        
        if not os.path.exists(email_dir):
            self.stdout.write(f"{Fore.YELLOW}📧 Email directory not found: {email_dir}{Style.RESET_ALL}")
            return
        
        email_files = glob.glob(os.path.join(email_dir, '*'))
        
        if not email_files:
            self.stdout.write(f"{Fore.YELLOW}📧 No email files found in: {email_dir}{Style.RESET_ALL}")
            return
        
        self.stdout.write(f"\n{Fore.CYAN}📧 EMAIL FILES{Style.RESET_ALL}")
        self.stdout.write(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        self.stdout.write(f"{Fore.YELLOW}Directory:{Style.RESET_ALL} {email_dir}")
        self.stdout.write("")
        
        for i, file_path in enumerate(sorted(email_files), 1):
            filename = os.path.basename(file_path)
            size = os.path.getsize(file_path)
            modified = os.path.getmtime(file_path)
            modified_time = timezone.datetime.fromtimestamp(modified).strftime('%Y-%m-%d %H:%M:%S')
            
            self.stdout.write(f"{Fore.GREEN}{i:2d}.{Style.RESET_ALL} {filename}")
            self.stdout.write(f"     {Fore.YELLOW}Size:{Style.RESET_ALL} {size} bytes")
            self.stdout.write(f"     {Fore.YELLOW}Modified:{Style.RESET_ALL} {modified_time}")
            self.stdout.write("")
        
        self.stdout.write(f"{Fore.BLUE}💡 Use --show-email FILENAME to view email content{Style.RESET_ALL}")

    def show_email_content(self, filename):
        """Show content of specific email file"""
        email_dir = os.path.join(settings.BASE_DIR, 'logs', 'emails')
        file_path = os.path.join(email_dir, filename)
        
        if not os.path.exists(file_path):
            self.stdout.write(f"{Fore.RED}❌ Email file not found: {filename}{Style.RESET_ALL}")
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.stdout.write(f"\n{Fore.CYAN}📧 EMAIL CONTENT: {filename}{Style.RESET_ALL}")
            self.stdout.write(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            self.stdout.write(content)
            self.stdout.write(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            
        except Exception as e:
            self.stdout.write(f"{Fore.RED}❌ Error reading email file: {e}{Style.RESET_ALL}")

    def cleanup_old_data(self):
        """Remove expired tokens and old email files"""
        # Remove expired tokens
        expired_tokens = EmailVerificationToken.objects.filter(
            created_at__lt=timezone.now() - timezone.timedelta(days=1)
        )
        expired_count = expired_tokens.count()
        expired_tokens.delete()
        
        # Remove old email files (older than 7 days)
        email_dir = os.path.join(settings.BASE_DIR, 'logs', 'emails')
        if os.path.exists(email_dir):
            email_files = glob.glob(os.path.join(email_dir, '*'))
            removed_files = 0
            
            for file_path in email_files:
                if os.path.getmtime(file_path) < timezone.now().timestamp() - (7 * 24 * 60 * 60):
                    os.remove(file_path)
                    removed_files += 1
            
            self.stdout.write(f"{Fore.GREEN}🧹 Cleanup completed:{Style.RESET_ALL}")
            self.stdout.write(f"  - Removed {expired_count} expired tokens")
            self.stdout.write(f"  - Removed {removed_files} old email files")
        else:
            self.stdout.write(f"{Fore.GREEN}🧹 Removed {expired_count} expired tokens{Style.RESET_ALL}")
