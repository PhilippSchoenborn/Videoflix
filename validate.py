#!/usr/bin/env python3
"""
🔍 Videoflix Backend - Validierungs-Script
=========================================

Prüft ob das Backend korrekt installiert und funktionsfähig ist.
"""

import requests
import subprocess
import json
import time
import os
from pathlib import Path

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

def check_docker_containers():
    """Prüft ob alle Docker-Container laufen"""
    print_header("🐳 DOCKER-CONTAINER PRÜFEN")
    
    try:
        result = subprocess.run(
            ["docker-compose", "ps", "--format", "json"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print_error("Docker-compose ist nicht verfügbar")
            return False
        
        containers = []
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                containers.append(json.loads(line))
        
        required_services = ['web', 'db', 'redis']
        running_services = []
        
        for container in containers:
            service = container.get('Service', '')
            state = container.get('State', '')
            
            if service in required_services:
                if state == 'running':
                    print_success(f"Service '{service}' läuft")
                    running_services.append(service)
                else:
                    print_error(f"Service '{service}' ist nicht aktiv (Status: {state})")
        
        missing_services = set(required_services) - set(running_services)
        if missing_services:
            print_error(f"Fehlende Services: {', '.join(missing_services)}")
            return False
        
        print_success("Alle Docker-Container laufen korrekt")
        return True
        
    except Exception as e:
        print_error(f"Fehler beim Prüfen der Container: {str(e)}")
        return False

def check_backend_api():
    """Prüft ob das Backend-API erreichbar ist"""
    print_header("🌐 BACKEND-API PRÜFEN")
    
    base_url = "http://localhost:8000"
    
    # Health-Check
    try:
        response = requests.get(f"{base_url}/admin/", timeout=10)
        if response.status_code == 200:
            print_success("Backend ist erreichbar")
        else:
            print_error(f"Backend antwortet mit Status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"Backend ist nicht erreichbar: {str(e)}")
        return False
    
    # API-Endpoints prüfen
    endpoints = [
        "/api/",
        "/api/register/",
        "/api/login/",
        "/api/videos/",
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code in [200, 405, 401]:  # 405 = Method not allowed ist OK
                print_success(f"Endpoint {endpoint} ist verfügbar")
            else:
                print_warning(f"Endpoint {endpoint} antwortet mit Status {response.status_code}")
        except requests.exceptions.RequestException as e:
            print_error(f"Endpoint {endpoint} ist nicht erreichbar: {str(e)}")
    
    return True

def check_admin_login():
    """Prüft ob Admin-Login funktioniert"""
    print_header("🔑 ADMIN-LOGIN PRÜFEN")
    
    try:
        session = requests.Session()
        
        # CSRF-Token holen
        response = session.get("http://localhost:8000/admin/login/", timeout=10)
        if response.status_code != 200:
            print_error("Admin-Login-Seite nicht erreichbar")
            return False
        
        # CSRF-Token extrahieren
        csrf_token = None
        for line in response.text.split('\n'):
            if 'csrfmiddlewaretoken' in line and 'value=' in line:
                csrf_token = line.split('value="')[1].split('"')[0]
                break
        
        if not csrf_token:
            print_error("CSRF-Token nicht gefunden")
            return False
        
        # Login-Versuch
        login_data = {
            'username': 'admin@test.com',
            'password': 'admin123456',
            'csrfmiddlewaretoken': csrf_token,
            'next': '/admin/'
        }
        
        response = session.post(
            "http://localhost:8000/admin/login/",
            data=login_data,
            timeout=10
        )
        
        if response.status_code == 200 and '/admin/' in response.url:
            print_success("Admin-Login funktioniert")
            return True
        else:
            print_error("Admin-Login fehlgeschlagen")
            return False
            
    except Exception as e:
        print_error(f"Fehler beim Admin-Login: {str(e)}")
        return False

def check_database():
    """Prüft die Datenbank-Verbindung"""
    print_header("🗄️  DATENBANK PRÜFEN")
    
    try:
        result = subprocess.run(
            ["docker-compose", "exec", "-T", "web", "python", "manage.py", "check", "--database", "default"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print_success("Datenbank-Verbindung funktioniert")
            return True
        else:
            print_error(f"Datenbank-Problem: {result.stderr}")
            return False
            
    except Exception as e:
        print_error(f"Fehler beim Datenbank-Check: {str(e)}")
        return False

def check_files():
    """Prüft wichtige Dateien"""
    print_header("📁 DATEIEN PRÜFEN")
    
    required_files = [
        '.env',
        'docker-compose.yml',
        'requirements.txt',
        'manage.py',
        'create_admin.py',
        'verify_admin.py',
    ]
    
    all_files_exist = True
    
    for file in required_files:
        if os.path.exists(file):
            print_success(f"Datei {file} vorhanden")
        else:
            print_error(f"Datei {file} fehlt")
            all_files_exist = False
    
    # Ordner prüfen
    required_dirs = [
        'logs',
        'media',
        'authentication',
        'videos',
        'core',
    ]
    
    for dir in required_dirs:
        if os.path.exists(dir):
            print_success(f"Ordner {dir} vorhanden")
        else:
            print_error(f"Ordner {dir} fehlt")
            all_files_exist = False
    
    return all_files_exist

def run_basic_tests():
    """Führt grundlegende Tests aus"""
    print_header("🧪 GRUNDLEGENDE TESTS")
    
    try:
        result = subprocess.run(
            ["docker-compose", "exec", "-T", "web", "python", "manage.py", "test", "authentication.tests", "--verbosity=0"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print_success("Grundlegende Tests erfolgreich")
            return True
        else:
            print_warning(f"Einige Tests fehlgeschlagen: {result.stderr}")
            return False
            
    except Exception as e:
        print_error(f"Fehler beim Ausführen der Tests: {str(e)}")
        return False

def print_summary(results):
    """Gibt eine Zusammenfassung aus"""
    print_header("📊 VALIDIERUNGS-ZUSAMMENFASSUNG")
    
    total_checks = len(results)
    passed_checks = sum(1 for result in results.values() if result)
    
    print(f"Gesamte Prüfungen: {total_checks}")
    print(f"Erfolgreich: {passed_checks}")
    print(f"Fehlgeschlagen: {total_checks - passed_checks}")
    
    if passed_checks == total_checks:
        print_success("\n🎉 ALLE PRÜFUNGEN ERFOLGREICH!")
        print_success("Das Backend ist vollständig funktionsfähig!")
    else:
        print_error(f"\n❌ {total_checks - passed_checks} PRÜFUNGEN FEHLGESCHLAGEN!")
        print_warning("Bitte beheben Sie die Probleme und führen Sie die Validierung erneut aus.")
    
    print("\n" + "="*60)
    print("DETAILLIERTE ERGEBNISSE:")
    print("="*60)
    
    for check, result in results.items():
        status = "✅ ERFOLGREICH" if result else "❌ FEHLGESCHLAGEN"
        print(f"{check}: {status}")

def main():
    """Hauptfunktion"""
    print_header("🔍 VIDEOFLIX BACKEND VALIDIERUNG")
    print("Prüft die vollständige Funktionsfähigkeit des Backends.")
    
    # Warten auf Container-Start
    print_info("Warte auf Container-Start...")
    time.sleep(3)
    
    # Alle Prüfungen ausführen
    results = {}
    
    results["Docker-Container"] = check_docker_containers()
    results["Wichtige Dateien"] = check_files()
    results["Datenbank-Verbindung"] = check_database()
    results["Backend-API"] = check_backend_api()
    results["Admin-Login"] = check_admin_login()
    results["Grundlegende Tests"] = run_basic_tests()
    
    # Zusammenfassung
    print_summary(results)

if __name__ == "__main__":
    main()
