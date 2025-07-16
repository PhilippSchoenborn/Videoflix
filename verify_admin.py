#!/usr/bin/env python3
"""
Script zur Verifizierung und Aktivierung des Admin-Users.
Aktiviert und verifiziert den Admin-User falls nötig.
"""

import os
import django
from django.contrib.auth import get_user_model

# Django Setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

User = get_user_model()

def verify_admin():
    """Aktiviert und verifiziert den Admin-User."""
    
    try:
        # Admin-User finden
        admin_user = User.objects.get(username='admin')
        
        # Status vor Änderung
        print("📋 Status vor Verifizierung:")
        print(f"   - Aktiv: {admin_user.is_active}")
        print(f"   - Superuser: {admin_user.is_superuser}")
        print(f"   - E-Mail verifiziert: {getattr(admin_user, 'is_email_verified', 'Attribut nicht vorhanden')}")
        
        # Aktiviert Admin-User
        admin_user.is_active = True
        admin_user.is_superuser = True
        
        # E-Mail-Verifizierung setzen (falls Attribut existiert)
        if hasattr(admin_user, 'is_email_verified'):
            admin_user.is_email_verified = True
        
        admin_user.save()
        
        print("\n✅ Admin-User erfolgreich verifiziert:")
        print(f"   - Username: {admin_user.username}")
        print(f"   - E-Mail: {admin_user.email}")
        print(f"   - Aktiv: {admin_user.is_active}")
        print(f"   - Superuser: {admin_user.is_superuser}")
        print(f"   - E-Mail verifiziert: {getattr(admin_user, 'is_email_verified', 'Attribut nicht vorhanden')}")
        
    except User.DoesNotExist:
        print("❌ Admin-User 'admin' wurde nicht gefunden.")
        print("💡 Führe zuerst 'python create_admin.py' aus.")
        
    except Exception as e:
        print(f"❌ Fehler beim Verifizieren des Admin-Users: {str(e)}")

if __name__ == "__main__":
    verify_admin()
