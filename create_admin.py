#!/usr/bin/env python3
"""
Script zum Erstellen eines Admin-Users für das Videoflix-Projekt.
Erstellt einen funktionierenden Admin-User mit korrekten Berechtigungen.
"""

import os
import django
from django.contrib.auth import get_user_model

# Django Setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

User = get_user_model()

def create_admin():
    """Erstellt einen Admin-User mit verifizierten Daten."""
    
    # Prüfen ob Admin-User bereits existiert
    if User.objects.filter(username='admin').exists():
        print("❌ Admin-User 'admin' existiert bereits.")
        admin_user = User.objects.get(username='admin')
        
        # Prüfen ob User aktiviert ist
        if not admin_user.is_active or not admin_user.is_email_verified:
            print("⚠️  Admin-User existiert, aber ist nicht aktiviert. Aktiviere...")
            admin_user.is_active = True
            admin_user.is_email_verified = True
            admin_user.save()
            print("✅ Admin-User aktiviert!")
        else:
            print("✅ Admin-User ist bereits vollständig aktiviert.")
        return
    
    if User.objects.filter(email='admin@test.com').exists():
        print("❌ Admin-User mit E-Mail 'admin@test.com' existiert bereits.")
        return
    
    try:
        # Erstellt Admin-User mit korrekten Berechtigungen
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123456',
            first_name='Admin',
            last_name='User'
        )
        
        # E-Mail-Verifizierung setzen
        admin_user.is_email_verified = True
        admin_user.is_active = True
        admin_user.save()
        
        print("✅ Admin-User erfolgreich erstellt:")
        print(f"   - Username: {admin_user.username}")
        print(f"   - E-Mail: {admin_user.email}")
        print(f"   - Passwort: admin123456")
        print(f"   - Aktiv: {admin_user.is_active}")
        print(f"   - Superuser: {admin_user.is_superuser}")
        print(f"   - E-Mail verifiziert: {admin_user.is_email_verified}")
        
    except Exception as e:
        print(f"❌ Fehler beim Erstellen des Admin-Users: {str(e)}")

if __name__ == "__main__":
    create_admin()
