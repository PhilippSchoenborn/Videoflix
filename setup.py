#!/usr/bin/env python3
"""
🎬 Videoflix Backend - Automatisches Setup Script
============================================

Dieses Script prüft das System und richtet das Backend automatisch ein.
Es führt alle notwendigen Schritte aus, um das Projekt startbereit zu machen.
"""

import os
import sys
import subprocess
import time
import django
from pathlib import Path

# Farben für die Ausgabe
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

def print_header(message):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{message}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def run_command(command, description, check_output=False):
    """Führt ein Kommando aus und gibt den Status zurück"""
    print_info(f"Führe aus: {description}")
    try:
        if check_output:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print_success(f"{description} - Erfolgreich")
                return True, result.stdout
            else:
                print_error(f"{description} - Fehlgeschlagen: {result.stderr}")
                return False, result.stderr
        else:
            result = subprocess.run(command, shell=True)
            if result.returncode == 0:
                print_success(f"{description} - Erfolgreich")
                return True, ""
            else:
                print_error(f"{description} - Fehlgeschlagen")
                return False, ""
    except Exception as e:
        print_error(f"{description} - Fehler: {str(e)}")
        return False, str(e)

def check_requirements():
    """Prüft die Systemanforderungen"""
    print_header("🔍 SYSTEMANFORDERUNGEN PRÜFEN")
    
    # Docker prüfen
    success, output = run_command("docker --version", "Docker Version prüfen", check_output=True)
    if not success:
        print_error("Docker ist nicht installiert oder nicht verfügbar!")
        print_info("Bitte installieren Sie Docker Desktop von: https://www.docker.com/products/docker-desktop")
        return False
    
    # Docker Compose prüfen
    success, output = run_command("docker-compose --version", "Docker Compose Version prüfen", check_output=True)
    if not success:
        print_error("Docker Compose ist nicht installiert!")
        return False
    
    # Python prüfen
    success, output = run_command("python --version", "Python Version prüfen", check_output=True)
    if not success:
        print_error("Python ist nicht installiert!")
        return False
    
    print_success("Alle Systemanforderungen erfüllt!")
    return True

def setup_environment():
    """Richtet die Umgebung ein"""
    print_header("⚙️  UMGEBUNG EINRICHTEN")
    
    # .env Datei prüfen
    if not os.path.exists('.env'):
        print_error(".env Datei nicht gefunden!")
        return False
    
    print_success(".env Datei gefunden")
    
    # Logs-Ordner erstellen
    os.makedirs('logs', exist_ok=True)
    print_success("Logs-Ordner erstellt")
    
    # Media-Ordner erstellen
    os.makedirs('media', exist_ok=True)
    os.makedirs('media/videos', exist_ok=True)
    os.makedirs('media/video_thumbnails', exist_ok=True)
    print_success("Media-Ordner erstellt")
    
    return True

def build_containers():
    """Baut die Docker-Container"""
    print_header("🐳 DOCKER-CONTAINER BAUEN")
    
    # Alte Container stoppen
    run_command("docker-compose down", "Alte Container stoppen")
    
    # Container neu bauen
    success, output = run_command("docker-compose up -d --build", "Container bauen und starten")
    if not success:
        print_error("Container konnten nicht gebaut werden!")
        return False
    
    # Warten bis Container bereit sind
    print_info("Warte auf Container-Start...")
    time.sleep(10)
    
    return True

def setup_database():
    """Richtet die Datenbank ein"""
    print_header("🗄️  DATENBANK EINRICHTEN")
    
    # Migrations erstellen
    success, output = run_command(
        "docker-compose exec -T web python manage.py makemigrations",
        "Migrations erstellen"
    )
    if not success:
        print_warning("Migrations konnten nicht erstellt werden - möglicherweise bereits vorhanden")
    
    # Migrations ausführen
    success, output = run_command(
        "docker-compose exec -T web python manage.py migrate",
        "Datenbank migrieren"
    )
    if not success:
        print_error("Datenbank-Migration fehlgeschlagen!")
        return False
    
    return True

def create_superuser():
    """Erstellt den Admin-User"""
    print_header("👤 ADMIN-USER ERSTELLEN")
    
    # Admin-User erstellen
    success, output = run_command(
        "docker-compose exec -T web python create_admin.py",
        "Admin-User erstellen"
    )
    if not success:
        print_warning("Admin-User konnte nicht erstellt werden - möglicherweise bereits vorhanden")
    
    # Admin-User verifizieren
    success, output = run_command(
        "docker-compose exec -T web python verify_admin.py",
        "Admin-User verifizieren"
    )
    if not success:
        print_warning("Admin-User konnte nicht verifiziert werden")
    
    return True

def run_tests():
    """Führt Tests aus"""
    print_header("🧪 TESTS AUSFÜHREN")
    
    success, output = run_command(
        "docker-compose exec -T web python manage.py test authentication.tests",
        "Authentication-Tests ausführen"
    )
    if not success:
        print_warning("Einige Tests sind fehlgeschlagen")
    
    return True

def print_final_info():
    """Gibt finale Informationen aus"""
    print_header("🎉 SETUP ABGESCHLOSSEN")
    
    print_success("Backend ist bereit!")
    print("")
    print(f"{Colors.BOLD}📋 WICHTIGE INFORMATIONEN:{Colors.END}")
    print(f"  • Backend URL: http://localhost:8000")
    print(f"  • Admin Panel: http://localhost:8000/admin")
    print(f"  • API Dokumentation: http://localhost:8000/api/")
    print("")
    print(f"{Colors.BOLD}🔑 ADMIN-ANMELDEDATEN:{Colors.END}")
    print(f"  • E-Mail: admin@test.com")
    print(f"  • Passwort: admin123456")
    print(f"  • Username: admin")
    print("")
    print(f"{Colors.BOLD}🐳 DOCKER-BEFEHLE:{Colors.END}")
    print(f"  • Container stoppen: docker-compose down")
    print(f"  • Container starten: docker-compose up -d")
    print(f"  • Logs anzeigen: docker-compose logs -f")
    print("")
    print(f"{Colors.BOLD}🛠️  NÜTZLICHE BEFEHLE:{Colors.END}")
    print(f"  • Shell öffnen: docker-compose exec web python manage.py shell")
    print(f"  • Tests ausführen: docker-compose exec web python manage.py test")
    print(f"  • Neuen Admin erstellen: docker-compose exec web python create_admin.py")

def main():
    """Hauptfunktion"""
    print_header("🎬 VIDEOFLIX BACKEND SETUP")
    print("Dieses Script richtet das Backend automatisch ein.")
    print("Bitte stellen Sie sicher, dass Docker Desktop läuft.")
    
    # Bestätigung
    response = input(f"\n{Colors.YELLOW}Möchten Sie mit dem Setup fortfahren? (j/n): {Colors.END}")
    if response.lower() not in ['j', 'ja', 'y', 'yes']:
        print("Setup abgebrochen.")
        return
    
    try:
        # Schritte ausführen
        if not check_requirements():
            return
        
        if not setup_environment():
            return
        
        if not build_containers():
            return
        
        if not setup_database():
            return
        
        if not create_superuser():
            return
        
        run_tests()
        
        print_final_info()
        
    except KeyboardInterrupt:
        print_error("\nSetup wurde unterbrochen.")
        print_info("Container können mit 'docker-compose down' gestoppt werden.")
    except Exception as e:
        print_error(f"Unerwarteter Fehler: {str(e)}")

if __name__ == "__main__":
    main()
