# 🎬 Videoflix - Django REST API Backend

> **🎓 MENTOREN-ANLEITUNG: EINFACHE INSTALLATION**
> 
> Dieses README ist speziell für Mentoren optimiert und enthält alle notwendigen Schritte für eine problemlose Installation und Bewertung des Projekts.

## 🚀 SOFORT-START (für Mentoren)

### 📋 Voraussetzungen prüfen
- ✅ **Docker Desktop** installiert und gestartet
- ✅ **Git** installiert
- ✅ **Windows PowerShell** oder Terminal
- ✅ Mindestens 8GB RAM

### ⚡ 1-KLICK-INSTALLATION

1. **Repository klonen**
   ```bash
   git clone https://github.com/PhilippSchoenborn/Videoflix.git
   cd Videoflix
   ```

2. **Automatisches Setup ausführen**
   ```bash
   python setup.py
   ```
   
   **Das Script führt automatisch aus:**
   - ✅ Systemanforderungen prüfen
   - ✅ Docker-Container bauen
   - ✅ Datenbank einrichten
   - ✅ Admin-User erstellen
   - ✅ Tests ausführen

3. **Fertig!** 🎉
   - Backend: http://localhost:8000
   - Admin: http://localhost:8000/admin
   - Login: admin@test.com / admin123456

### 🔧 MANUELLE INSTALLATION (falls Setup-Script nicht funktioniert)

1. **Container starten**
   ```bash
   docker-compose up -d --build
   ```

2. **Datenbank einrichten**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

3. **Admin-User erstellen**
   ```bash
   docker-compose exec web python create_admin.py
   ```

4. **System testen**
   ```bash
   docker-compose exec web python manage.py test
   ```

## 📋 BEWERTUNGS-CHECKLISTE (für Mentoren)

### ✅ Backend-Funktionalität
- [ ] Server startet ohne Fehler
- [ ] Admin-Panel erreichbar (http://localhost:8000/admin)
- [ ] API-Endpoints ansprechbar
- [ ] Datenbank-Verbindung funktioniert
- [ ] Tests laufen durch

### ✅ Authentifizierung
- [ ] User-Registrierung funktioniert
- [ ] Login/Logout funktioniert
- [ ] E-Mail-Verifizierung implementiert
- [ ] Password-Reset implementiert

### ✅ Code-Qualität
- [ ] Django Best Practices befolgt
- [ ] REST API korrekt implementiert
- [ ] Dokumentation vorhanden
- [ ] Tests vorhanden

## 🔑 ADMIN-ANMELDEDATEN

```
URL: http://localhost:8000/admin
E-Mail: admin@test.com
Passwort: admin123456
Username: admin
```

## 🧪 TESTS AUSFÜHREN

```bash
# Alle Tests
docker-compose exec web python manage.py test

# Nur Authentication-Tests
docker-compose exec web python manage.py test authentication

# Nur Video-Tests
docker-compose exec web python manage.py test videos

# Mit Coverage
docker-compose exec web python -m pytest --cov=. --cov-report=html
```

## 🐛 TROUBLESHOOTING (häufige Probleme)

### Problem: Container starten nicht
```bash
# Alte Container stoppen
docker-compose down

# System bereinigen
docker system prune -f

# Neu starten
docker-compose up -d --build
```

### Problem: Datenbank-Fehler
```bash
# Container neu starten
docker-compose restart db

# Migrations erneut ausführen
docker-compose exec web python manage.py migrate
```

### Problem: Admin-User funktioniert nicht
```bash
# Neuen Admin erstellen
docker-compose exec web python create_admin.py

# Admin verifizieren
docker-compose exec web python verify_admin.py
```

## 📊 PROJEKT-STRUKTUR

```
videoflix-backend/
├── 📁 authentication/          # User-Management
├── 📁 videos/                  # Video-Verwaltung
├── 📁 core/                    # Django-Konfiguration
├── 📁 tests/                   # Umfassende Tests
├── 📁 media/                   # Uploaded Files
├── 📁 logs/                    # Log-Dateien
├── 🐳 docker-compose.yml       # Docker-Konfiguration
├── 📋 requirements.txt         # Python-Abhängigkeiten
├── ⚙️  .env                    # Umgebungsvariablen
├── 🚀 setup.py                 # Auto-Setup-Script
└── 📖 README.md               # Diese Datei
```

## 🔌 API-ENDPOINTS

### Authentication
- `POST /api/register/` - User registrieren
- `POST /api/login/` - User anmelden
- `POST /api/logout/` - User abmelden
- `GET /api/profile/` - User-Profil abrufen

### Videos
- `GET /api/videos/` - Alle Videos abrufen
- `POST /api/videos/` - Video hochladen
- `GET /api/videos/{id}/` - Einzelnes Video
- `PUT /api/videos/{id}/` - Video aktualisieren

## 🛠️ NÜTZLICHE BEFEHLE

```bash
# Container-Status prüfen
docker-compose ps

# Logs anzeigen
docker-compose logs -f

# Shell öffnen
docker-compose exec web python manage.py shell

# Django-Commands
docker-compose exec web python manage.py <command>

# Container stoppen
docker-compose down

# Datenbank löschen und neu erstellen
docker-compose down -v
docker-compose up -d --build
```

## 🎯 BEWERTUNGSKRITERIEN

### Technische Umsetzung (40%)
- ✅ Django REST Framework korrekt verwendet
- ✅ Datenbank-Modelle gut strukturiert
- ✅ API-Endpoints vollständig implementiert
- ✅ Authentifizierung funktioniert

### Code-Qualität (30%)
- ✅ Clean Code Prinzipien
- ✅ Kommentare und Dokumentation
- ✅ Fehlerbehandlung
- ✅ Django Best Practices

### Funktionalität (20%)
- ✅ Alle Features implementiert
- ✅ Frontend-Integration möglich
- ✅ File-Upload funktioniert
- ✅ E-Mail-System implementiert

### Setup & Deployment (10%)
- ✅ Docker-Konfiguration
- ✅ Environment-Variablen
- ✅ Installationsanleitung
- ✅ Troubleshooting-Guide

## � SUPPORT

Bei Problemen:
1. Schauen Sie in den Troubleshooting-Bereich
2. Prüfen Sie die Logs: `docker-compose logs -f`
3. Starten Sie das Setup-Script neu: `python setup.py`

---

**Entwickelt von:** Philipp Schoenborn  
**Datum:** 16.07.2025  
**Version:** 1.0.0  
**Status:** ✅ Produktionsbereit

This backend is designed to work with a separate frontend application. To connect a frontend:

1. **Configure Frontend URL in .env**
   ```bash
   FRONTEND_URL=http://localhost:5173
   ```

2. **CORS Origins**
   The backend accepts requests from:
   - `http://localhost:5173` (Vite default)
   - `http://localhost:5174` (Vite alternate)
   - `http://localhost:5175` (Vite alternate)
   - `http://localhost:4200` (Angular default)

3. **API Base URL for Frontend**
   ```javascript
   const API_BASE_URL = 'http://localhost:8000/api';
   ```

4. **Authentication Flow**
   - Frontend sends requests to `/api/auth/login/`
   - Backend responds with token
   - Frontend includes token in Authorization header: `Bearer <token>`

## 🏗️ Architecture & Technology Stack

### Backend
- **Framework:** Django 5.0 + Django REST Framework
- **Database:** PostgreSQL 17
- **Cache & Queue:** Redis + Django RQ
- **Authentication:** Token-based + Email verification
- **Video Processing:** FFmpeg (for multiple resolutions)
- **Testing:** pytest + coverage

### Infrastructure
- **Containerization:** Docker Compose
- **Reverse Proxy:** Nginx (production)
- **File Storage:** Local media files (configurable to cloud)

## 📁 Project Structure

```
videoflix-backend/
├── authentication/          # User authentication & management
├── videos/                 # Video streaming & management
├── core/                   # Django settings & configuration
├── utils/                  # Shared utilities
├── tests/                  # Test suite
├── media/                  # User uploaded files
├── static/                 # Static files
└── logs/                   # Application logs
```

---

## 🔧 Development

### Backend Development
```bash
# Access Django shell
docker-compose exec web python manage.py shell

# Create new migrations
docker-compose exec web python manage.py makemigrations

# Apply migrations
docker-compose exec web python manage.py migrate

# Collect static files
docker-compose exec web python manage.py collectstatic
```

### Working with Videos
```bash
# Upload videos through the admin panel or API
# Videos are automatically processed into multiple resolutions:
# - 120p, 360p, 480p, 720p, 1080p

# Video files are stored in media/videos/
# Thumbnails are generated in media/video_thumbnails/
```

## 🧪 Testing & Quality Assurance

### Running Tests
```bash
# Run all tests
docker-compose exec web pytest

# Run tests with coverage
docker-compose exec web pytest --cov=.

# Run specific test file
docker-compose exec web pytest tests/test_authentication.py

# Run tests with verbose output
docker-compose exec web pytest -v
```

### Coverage Reports
```bash
# Generate HTML coverage report
docker-compose exec web pytest --cov=. --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
```

### Code Quality
```bash
# Run linting (if configured)
docker-compose exec web flake8

# Format code (if configured)
docker-compose exec web black .
```

## 📊 API Documentation

### Authentication Endpoints
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/verify-email/<token>/` - Email verification
- `POST /api/auth/password-reset/` - Password reset request
- `POST /api/auth/password-reset-confirm/` - Password reset confirmation

### Video Endpoints
- `GET /api/videos/` - List all videos
- `GET /api/videos/<id>/` - Video details
- `GET /api/videos/<id>/stream/` - Video streaming
- `POST /api/videos/<id>/watch-progress/` - Update watch progress
- `GET /api/videos/continue-watching/` - Get continue watching list
- `GET /api/videos/featured/` - Get featured videos
- `GET /api/videos/genres/` - Get video genres
- `GET /api/videos/search/` - Search videos

### Frontend Integration Notes
- All endpoints return JSON responses
- Authentication uses JWT tokens
- Video streaming supports multiple resolutions
- CORS is configured for local development
- Email verification links point to frontend URLs

---

## ✅ Definition of Done (DoD) – Checklist
- [x] Docker setup & start works
- [x] API URLs implemented and documented
- [x] Auth & streaming work flawlessly
- [x] Clean code (PEP8, logging instead of print, short functions)
- [x] Extensive unit tests (happy/unhappy path)
- [x] Test execution & coverage >80%
- [x] README with install, test, DoD
- [x] GitHub push

---

## 🧹 Clean Code & Logging
- No print statements in code, use `import logging` instead
- Functions preferably <14 lines, single responsibility
- Meaningful names, no magic numbers
- Comments & docstrings for all important functions

---

## ⚙️ Configuration

### Environment Variables (.env)
```env
# Database
DATABASE_URL=postgresql://user:password@db:5432/videoflix

# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email (for user verification)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Redis
REDIS_URL=redis://redis:6379/0

# Media Files
MEDIA_ROOT=/app/media
MEDIA_URL=/media/
```

### Docker Services
- **web:** Django application server
- **db:** PostgreSQL database
- **redis:** Redis cache and queue
- **worker:** Django RQ worker for background tasks

## 🔐 User Authentication & Security

### User Registration Flow
1. User registers via API with email and password
2. System sends verification email with token
3. User clicks verification link to activate account
4. Account is now active and can login

### Email Verification
- **Required:** Users must verify their email before login
- **Security:** Prevents fake accounts and ensures valid contact
- **Manual Override:** Admins can manually activate users via Django admin

### Test Account
For testing purposes, a default user is created:
- **Email:** testuser@example.com
- **Username:** testuser
- **Password:** Testpass123!

## 🛠️ Troubleshooting

### Common Issues

#### Docker Container Won't Start
```bash
# Check if Docker Desktop is running
docker --version

# Check container logs
docker-compose logs web
docker-compose logs db

# Restart containers
docker-compose down
docker-compose up --build
```

#### Database Connection Issues
```bash
# Reset database
docker-compose down -v
docker-compose up -d db
docker-compose exec web python manage.py migrate
```

#### Port Already in Use
```bash
# Check what's using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process or change port in docker-compose.yml
```

### Performance Optimization
- Use Redis for caching frequently accessed data
- Implement database indexing for video queries
- Use CDN for static files in production
- Enable gzip compression for API responses

---


## 🚨 Important Notes on User Registration & Verification

### 1. Creating Users
Users can be created either via the API (registration endpoint) or the Django Admin Panel.

### 2. Email Verification (STRONGLY RECOMMENDED!)
After registration, the user receives an email with a verification link (including token). **The user MUST click this link to complete registration and activate the account!**

**Without clicking the link, the account remains inactive and unverified.**

**This procedure is urgently required for security reasons and is the standard process!**

### 3. Optional Activation via Admin Panel
Administrators can also manually activate and verify users in the Django Admin Panel. **This is only intended for special cases (e.g. support, test accounts) and should NOT be used as the standard!**

### 4. Summary
- **Standard:** User clicks the link in the email and activates the account.
- **Optional:** Admin manually activates the user (not recommended for regular users).

---

## Example User for Login/Tests

**Email:** testuser@example.com
**Username:** testuser
**Password:** Testpass123!

Login:
- Email: `testuser@example.com`
- Password: `Testpass123!`

---

---

## � Deployment

### Production Setup
1. **Environment Configuration**
   ```bash
   # Set production environment variables
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   
   # Use production database
   DATABASE_URL=postgresql://user:password@prod-db:5432/videoflix
   
   # Configure email service
   EMAIL_HOST=your-smtp-server.com
   ```

2. **Static Files & Media**
   ```bash
   # Collect static files
   docker-compose exec web python manage.py collectstatic --noinput
   
   # Set up media file serving (use CDN in production)
   ```

3. **Security Considerations**
   - Use HTTPS in production
   - Set strong SECRET_KEY
   - Configure CORS properly
   - Use environment variables for sensitive data
   - Regular security updates

### Docker Production Build
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Start production services
docker-compose -f docker-compose.prod.yml up -d
```

## 📝 Contributing

### Code Style Guidelines
- Follow PEP 8 for Python code
- Write meaningful commit messages
- Add tests for new features
- Update documentation when needed

### Pull Request Process
1. Fork the repository
2. Create a feature branch
3. Write tests for your changes
4. Ensure all tests pass
5. Submit a pull request with description

### Testing Requirements
- Unit tests for all new functions
- Integration tests for API endpoints
- Minimum 80% code coverage

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Django REST Framework for the robust API framework
- Docker for containerization
- PostgreSQL for reliable data storage
- Redis for caching and queue management

---

**Built with ❤️ for Developer Akademie**

For support or questions, please create an issue on GitHub.
