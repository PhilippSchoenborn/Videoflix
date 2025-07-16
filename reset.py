#!/usr/bin/env python3
"""
🔄 Videoflix Backend - Reset Script
==================================

Dieses Script setzt das gesamte Backend zurück und behebt häufige Probleme.
"""

import subprocess
import time
import os

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

def run_command(command, description):
    """Führt ein Kommando aus und gibt den Status zurück"""
    print_info(f"Führe aus: {description}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print_success(f"{description} - Erfolgreich")
            return True
        else:
            print_error(f"{description} - Fehlgeschlagen: {result.stderr}")
            return False
    except Exception as e:
        print_error(f"{description} - Fehler: {str(e)}")
        return False

def reset_system():
    """Setzt das gesamte System zurück"""
    print_header("🔄 SYSTEM-RESET")
    
    # 1. Container stoppen
    run_command("docker-compose down", "Container stoppen")
    
    # 2. Volumes löschen
    print_warning("Lösche alle Datenbank-Volumes (alle Daten gehen verloren!)")
    run_command("docker-compose down -v", "Volumes löschen")
    
    # 3. Docker-System bereinigen
    run_command("docker system prune -f", "Docker-System bereinigen")
    
    # 4. Container neu bauen
    run_command("docker-compose up -d --build", "Container neu bauen")
    
    # 5. Warten
    print_info("Warte auf Container-Start...")
    time.sleep(20)
    
    # 6. Migrationen ausführen
    run_command("docker-compose exec -T web python manage.py migrate", "Datenbank migrieren")
    
    # 7. Admin-User erstellen
    run_command("docker-compose exec -T web python create_admin.py", "Admin-User erstellen")
    
    # 8. Admin-User verifizieren
    run_command("docker-compose exec -T web python verify_admin.py", "Admin-User verifizieren")
    
    print_header("✅ SYSTEM-RESET ABGESCHLOSSEN")
    print_success("System wurde erfolgreich zurückgesetzt!")
    print("")
    print("📋 Zugangsdaten:")
    print("  • Backend: http://localhost:8000")
    print("  • Admin: http://localhost:8000/admin")
    print("  • Login: admin@test.com / admin123456")

def main():
    """Hauptfunktion"""
    print_header("🔄 VIDEOFLIX BACKEND RESET")
    print("Dieses Script setzt das gesamte Backend zurück.")
    print_warning("WARNUNG: Alle Daten in der Datenbank gehen verloren!")
    
    # Bestätigung
    response = input(f"\n{Colors.YELLOW}Möchten Sie das System zurücksetzen? (j/n): {Colors.END}")
    if response.lower() not in ['j', 'ja', 'y', 'yes']:
        print("Reset abgebrochen.")
        return
    
    reset_system()

if __name__ == "__main__":
    main()
