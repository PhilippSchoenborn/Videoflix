from authentication.models import CustomUser, EmailVerificationToken
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

users = CustomUser.objects.all()
tokens = EmailVerificationToken.objects.all()

print('USERS:')
for u in users:
    print(f'{u.email} | is_active={u.is_active} | is_email_verified={u.is_email_verified}')

print('\nVERIFICATION LINKS:')
for t in tokens:
    uidb64 = urlsafe_base64_encode(force_bytes(t.user.pk))
    print(f'{t.user.email}: http://localhost:8000/api/verify-email/{uidb64}/{t.token}/')
