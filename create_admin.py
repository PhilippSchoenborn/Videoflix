#!/usr/bin/env python3
"""
Script to create an admin user for the Videoflix project.
Creates a working admin user with correct permissions.
"""

import os
import django
from django.contrib.auth import get_user_model

# Django Setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

User = get_user_model()

def create_admin():
    """Creates an admin user with verified data."""
    
    # Check if admin user already exists
    if User.objects.filter(username='admin').exists():
        print("❌ Admin user 'admin' already exists.")
        return
    
    if User.objects.filter(email='admin@test.com').exists():
        print("❌ Admin user with email 'admin@test.com' already exists.")
        return
    
    try:
        # Create admin user with correct permissions
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123456',
            first_name='Admin',
            last_name='User'
        )
        
        # Set email verification
        admin_user.is_email_verified = True
        admin_user.is_active = True
        admin_user.save()
        
        print("✅ Admin user successfully created:")
        print(f"   - Username: {admin_user.username}")
        print(f"   - Email: {admin_user.email}")
        print(f"   - Password: admin123456")
        print(f"   - Active: {admin_user.is_active}")
        print(f"   - Superuser: {admin_user.is_superuser}")
        print(f"   - Email verified: {admin_user.is_email_verified}")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {str(e)}")

if __name__ == "__main__":
    create_admin()
