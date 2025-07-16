#!/usr/bin/env python3
"""
Script to verify and activate the admin user.
Activates and verifies the admin user if needed.
"""

import os
import django
from django.contrib.auth import get_user_model

# Django Setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

User = get_user_model()

def verify_admin():
    """Activates and verifies the admin user."""
    
    try:
        # Find admin user
        admin_user = User.objects.get(username='admin')
        
        # Status before changes
        print("📋 Status before verification:")
        print(f"   - Active: {admin_user.is_active}")
        print(f"   - Superuser: {admin_user.is_superuser}")
        print(f"   - Email verified: {getattr(admin_user, 'is_email_verified', 'Attribute not available')}")
        
        # Activate admin user
        admin_user.is_active = True
        admin_user.is_superuser = True
        
        # Set email verification (if attribute exists)
        if hasattr(admin_user, 'is_email_verified'):
            admin_user.is_email_verified = True
        
        admin_user.save()
        
        print("\n✅ Admin user successfully verified:")
        print(f"   - Username: {admin_user.username}")
        print(f"   - Email: {admin_user.email}")
        print(f"   - Active: {admin_user.is_active}")
        print(f"   - Superuser: {admin_user.is_superuser}")
        print(f"   - Email verified: {getattr(admin_user, 'is_email_verified', 'Attribute not available')}")
        
    except User.DoesNotExist:
        print("❌ Admin user 'admin' was not found.")
        print("💡 Run 'python create_admin.py' first.")
        
    except Exception as e:
        print(f"❌ Error verifying admin user: {str(e)}")

if __name__ == "__main__":
    verify_admin()
