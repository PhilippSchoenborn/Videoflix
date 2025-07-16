# 🎓 MENTOREN-ANLEITUNG - VIDEOFLIX BACKEND

> **⚡ SCHNELLSTART: 3 MINUTEN ZUM LAUFENDEN SYSTEM**

## 🚀 SOFORT-INSTALLATION

### Option 1: Automatisches Setup (Empfohlen)
```bash
# 1. Repository klonen
git clone https://github.com/PhilippSchoenborn/Videoflix.git
cd Videoflix

# 2. Automatisches Setup starten
python setup.py

# 3. Fertig! System ist bereit
```

### Option 2: Windows-Batch-Datei
```bash
# Doppelklick auf start.bat
# Oder in PowerShell:
.\start.bat
```

### Option 3: Manuelle Installation
```bash
# 1. Container starten
docker-compose up -d --build

# 2. Datenbank einrichten
docker-compose exec web python manage.py migrate

# 3. Admin-User erstellen
docker-compose exec web python create_admin.py

# 4. System validieren
python validate.py
```

## 📋 SYSTEM-ZUGANG

| Service | URL | Anmeldedaten |
|---------|-----|-------------|
| **Backend API** | http://localhost:8000 | - |
| **Admin Panel** | http://localhost:8000/admin | admin@test.com / admin123456 |
| **API Docs** | http://localhost:8000/api/ | - |

## ✅ SYSTEM-VALIDIERUNG

```bash
# Vollständige Validierung
python validate.py

# Manuell prüfen
curl http://localhost:8000/admin/
curl http://localhost:8000/api/

# Container-Status
docker-compose ps
```

## 🧪 TESTS AUSFÜHREN

```bash
# Alle Tests
docker-compose exec web python manage.py test

# Nur wichtige Tests
docker-compose exec web python manage.py test authentication
docker-compose exec web python manage.py test videos

# Mit Coverage
docker-compose exec web python -m pytest --cov=.
```

## 📊 BEWERTUNGSKRITERIEN

### ✅ Funktionalität (40 Punkte)
- [ ] Server startet fehlerfrei
- [ ] Admin-Panel funktioniert
- [ ] API-Endpoints ansprechbar
- [ ] Datenbank-Verbindung
- [ ] User-Authentifizierung
- [ ] Video-Upload/Management
- [ ] E-Mail-Verifizierung
- [ ] Password-Reset

### ✅ Code-Qualität (30 Punkte)
- [ ] Django Best Practices
- [ ] REST API Design
- [ ] Datenbank-Modelle
- [ ] Fehlerbehandlung
- [ ] Kommentare/Dokumentation
- [ ] Tests vorhanden
- [ ] Security-Implementierung

### ✅ Setup & Deployment (20 Punkte)
- [ ] Docker-Konfiguration
- [ ] Environment-Variablen
- [ ] Installationsanleitung
- [ ] Automatisierung
- [ ] Troubleshooting-Guide

### ✅ Zusatzfunktionen (10 Punkte)
- [ ] Video-Processing
- [ ] Background-Tasks
- [ ] Caching (Redis)
- [ ] File-Management
- [ ] API-Pagination

## 🐛 HÄUFIGE PROBLEME & LÖSUNGEN

### Problem: Container starten nicht
```bash
# Lösung 1: System bereinigen
docker-compose down -v
docker system prune -f
docker-compose up -d --build

# Lösung 2: Docker neu starten
# Docker Desktop neu starten
```

### Problem: Admin-Login funktioniert nicht
```bash
# Lösung: Neuen Admin erstellen
docker-compose exec web python create_admin.py
docker-compose exec web python verify_admin.py
```

### Problem: API nicht erreichbar
```bash
# Lösung: Container-Status prüfen
docker-compose ps
docker-compose logs web

# Container neu starten
docker-compose restart web
```

### Problem: Datenbank-Fehler
```bash
# Lösung: Datenbank neu initialisieren
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py check --database default
```

## 🔧 NÜTZLICHE BEFEHLE

```bash
# Container-Management
docker-compose ps                 # Status anzeigen
docker-compose logs -f web        # Logs verfolgen
docker-compose exec web bash      # Shell öffnen
docker-compose down               # Stoppen
docker-compose up -d --build      # Neu starten

# Django-Commands
docker-compose exec web python manage.py shell
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic
docker-compose exec web python manage.py test

# System-Diagnose
python validate.py                # Vollständige Validierung
docker-compose exec web python manage.py check
curl -I http://localhost:8000/admin/
```

## 📁 PROJEKT-STRUKTUR

```
videoflix-backend/
├── 🚀 setup.py              # Automatisches Setup
├── 🔍 validate.py           # System-Validierung
├── 📊 start.bat             # Windows-Schnellstart
├── 📋 MENTOREN-ANLEITUNG.md # Diese Datei
├── 🐳 docker-compose.yml    # Container-Konfiguration
├── 📦 requirements.txt      # Python-Abhängigkeiten
├── ⚙️  .env                 # Umgebungsvariablen
├── 🏗️  backend.Dockerfile   # Backend-Container
├── 🎯 manage.py             # Django-Management
├── 👤 create_admin.py       # Admin-User-Setup
├── ✅ verify_admin.py       # Admin-User-Verifizierung
├── 📁 authentication/       # User-Management
├── 📁 videos/              # Video-Verwaltung
├── 📁 core/                # Django-Konfiguration
├── 📁 tests/               # Umfassende Tests
├── 📁 media/               # Uploaded Files
└── 📁 logs/                # Log-Dateien
```

## 🎯 BEWERTUNGSMATRIX

| Kriterium | Gewichtung | Prüfung |
|-----------|------------|---------|
| **Installation** | 10% | `python setup.py` funktioniert |
| **Container** | 10% | `docker-compose ps` zeigt alle Services |
| **Database** | 15% | `python validate.py` - DB-Test |
| **API** | 20% | Alle Endpoints erreichbar |
| **Authentication** | 15% | Login/Register funktioniert |
| **Admin** | 10% | Admin-Panel funktioniert |
| **Tests** | 10% | `manage.py test` läuft durch |
| **Code-Quality** | 10% | Clean Code, Kommentare |

## 📞 SUPPORT

**Bei Problemen:**
1. `python validate.py` ausführen
2. `docker-compose logs -f` prüfen
3. `python setup.py` erneut ausführen
4. Troubleshooting-Guide konsultieren

**System-Requirements:**
- Docker Desktop (läuft)
- 8GB RAM minimum
- 5GB freier Speicher
- Windows 10/11 oder macOS/Linux

---

**Entwickelt für:** Developer Akademie  
**Mentor-Review:** Bereit für Bewertung  
**Datum:** 16.07.2025  
**Version:** 1.0 - Production Ready ✅
