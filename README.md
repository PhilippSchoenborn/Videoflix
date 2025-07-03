# 🎬 Videoflix - Backend API

A modern video streaming platform backend built with Django REST Framework, featuring user authentication, video management, and background processing capabilities.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)

## ✨ Features

### 🔐 Authentication & User Management
- User registration with email verification
- Secure login/logout with token authentication
- Password reset functionality
- Custom user model with profile management
- Email verification system

### 🎥 Video Management
- Video upload and processing
- Multiple quality transcoding (120p, 360p, 720p, 1080p)
- Thumbnail generation
- Genre-based categorization
- Featured videos system
- Video streaming with quality selection

### 📱 User Experience
- Watch progress tracking
- Continue watching functionality
- Responsive video player support
- Search and filtering capabilities
- Genre-based video organization

### ⚡ Performance & Scalability
- Redis caching layer
- Background task processing with RQ
- PostgreSQL database
- Docker containerization
- Static file optimization

## 🛠 Tech Stack

- **Backend Framework**: Django 5.2.4 + Django REST Framework
- **Database**: PostgreSQL 17
- **Cache/Queue**: Redis
- **Task Queue**: Django RQ
- **Authentication**: Token-based authentication
- **File Processing**: FFmpeg for video processing
- **Containerization**: Docker & Docker Compose
- **Testing**: pytest + coverage
- **Code Quality**: PEP 8 compliant

## 🚀 Getting Started

### Prerequisites

- Docker Desktop installed and running
- Git
- 8GB+ RAM recommended

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd videoflix-backend
   ```

2. **Environment Setup**
   ```bash
   cp .env.template .env
   # Edit .env with your configuration
   ```

3. **Start with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Run Migrations**
   ```bash
   docker exec videoflix-web python manage.py migrate
   ```

5. **Create Superuser**
   ```bash
   docker exec -it videoflix-web python manage.py createsuperuser
   ```

6. **Access the Application**
   - API: http://localhost:8000
   - Admin: http://localhost:8000/admin
   - API Documentation: http://localhost:8000/api/

## 📚 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | User registration |
| POST | `/api/auth/login/` | User login |
| POST | `/api/auth/logout/` | User logout |
| GET | `/api/auth/verify-email/<token>/` | Email verification |
| POST | `/api/auth/password-reset-request/` | Request password reset |
| POST | `/api/auth/password-reset/` | Reset password |
| GET/PUT | `/api/auth/profile/` | User profile |

### Video Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/videos/` | List videos |
| GET | `/api/videos/<id>/` | Video details |
| GET | `/api/videos/featured/` | Featured videos |
| GET | `/api/videos/by-genre/` | Videos grouped by genre |
| POST | `/api/videos/upload/` | Upload video |
| GET | `/api/videos/<id>/stream/<quality>/` | Stream video |
| GET | `/api/videos/<id>/qualities/` | Available qualities |

### Watch Progress Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/videos/progress/` | User's watch progress |
| POST | `/api/videos/<id>/progress/` | Update watch progress |
| GET | `/api/videos/continue-watching/` | Continue watching list |

### Genre Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/videos/genres/` | List all genres |

## 💻 Development

### Project Structure

```
videoflix-backend/
├── authentication/          # User authentication app
│   ├── models.py           # Custom user model
│   ├── views.py            # Authentication views
│   ├── serializers.py      # API serializers
│   ├── utils.py            # Utility functions
│   └── urls.py             # URL configuration
├── videos/                 # Video management app
│   ├── models.py           # Video, Genre, WatchProgress models
│   ├── views.py            # Video API views
│   ├── serializers.py      # Video serializers
│   ├── utils.py            # Video processing utilities
│   └── urls.py             # URL configuration
├── utils/                  # Shared utilities
│   └── utils.py            # Common utility functions
├── core/                   # Django project settings
│   ├── settings.py         # Main configuration
│   ├── urls.py             # Root URL configuration
│   └── wsgi.py             # WSGI configuration
├── templates/              # Email templates
├── tests/                  # Test cases
├── static/                 # Static files
├── media/                  # User uploaded files
├── docker-compose.yml      # Docker services
├── backend.Dockerfile      # Backend container
├── requirements.txt        # Python dependencies
└── manage.py              # Django management script
```

### Local Development

1. **Install dependencies**
   ```bash
   docker exec videoflix-web pip install -r requirements.txt
   ```

2. **Run migrations**
   ```bash
   docker exec videoflix-web python manage.py makemigrations
   docker exec videoflix-web python manage.py migrate
   ```

3. **Collect static files**
   ```bash
   docker exec videoflix-web python manage.py collectstatic --noinput
   ```

4. **Access container shell**
   ```bash
   docker exec -it videoflix-web bash
   ```

### Code Quality Standards

- **PEP 8 Compliance**: All code follows Python PEP 8 standards
- **Function Length**: Maximum 14 lines per function
- **Single Responsibility**: Each function performs exactly one task
- **Naming Convention**: snake_case for functions and variables
- **Documentation**: All functions and classes are documented
- **No Dead Code**: All variables and functions are used

## 🧪 Testing

### Running Tests

```bash
# Run all tests
docker exec videoflix-web pytest

# Run with coverage
docker exec videoflix-web pytest --cov=.

# Run specific test file
docker exec videoflix-web pytest tests/test_authentication.py

# Generate HTML coverage report
docker exec videoflix-web pytest --cov=. --cov-report=html
```

### Test Coverage

The project maintains **80%+ test coverage** with comprehensive test suites for:

- ✅ Authentication (registration, login, password reset)
- ✅ Video management (CRUD operations, streaming)
- ✅ Watch progress tracking
- ✅ API endpoints
- ✅ Model functionality
- ✅ Utility functions

### Test Structure

- `tests/test_authentication.py` - Authentication tests
- `tests/test_videos.py` - Video functionality tests
- `tests/__init__.py` - Test base classes and fixtures

## 🐳 Docker Services

The application runs with the following Docker services:

### Web Service (Django)
- **Port**: 8000
- **Features**: Django application with Gunicorn
- **Dependencies**: PostgreSQL, Redis
- **Health Check**: HTTP endpoint monitoring

### Database Service (PostgreSQL)
- **Port**: 5432
- **Database**: videoflix_db
- **User**: videoflix_user
- **Persistence**: Named volume

### Cache Service (Redis)
- **Port**: 6379
- **Purpose**: Caching and task queue
- **Configuration**: Optimized for performance

### Background Workers
- **Service**: RQ Workers
- **Purpose**: Video processing, email sending
- **Scaling**: Can be horizontally scaled

## 🔧 Configuration

### Environment Variables

Key environment variables in `.env`:

```env
# Django Settings
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=videoflix_db
DB_USER=videoflix_user
DB_PASSWORD=your-db-password
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

# Email
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-password

# Frontend
FRONTEND_URL=http://localhost:4200
```

### Video Processing

- **Supported Formats**: MP4, AVI, MOV, WMV
- **Output Qualities**: 120p, 360p, 720p, 1080p
- **Processing**: Asynchronous with RQ
- **Storage**: Local filesystem (configurable)

## 📈 Performance

### Optimization Features

- **Database Indexing**: Optimized queries with proper indexes
- **Caching**: Redis for frequently accessed data
- **Background Processing**: Non-blocking video processing
- **Static Files**: Whitenoise for efficient static file serving
- **Connection Pooling**: Optimized database connections

### Monitoring

- **Logging**: Comprehensive logging system
- **Health Checks**: Service availability monitoring
- **Metrics**: Performance tracking capabilities

## 🚀 Deployment

### Production Considerations

1. **Security**
   - Set `DEBUG=False`
   - Use strong `SECRET_KEY`
   - Configure HTTPS
   - Set up proper CORS headers

2. **Database**
   - Use managed PostgreSQL service
   - Configure backups
   - Set up monitoring

3. **Media Storage**
   - Consider cloud storage (AWS S3, etc.)
   - CDN for video delivery
   - Backup strategy

4. **Scaling**
   - Horizontal scaling for web workers
   - Dedicated RQ workers
   - Load balancing

### Docker Production

```bash
# Production build
docker-compose -f docker-compose.prod.yml up -d

# Scale workers
docker-compose -f docker-compose.prod.yml up -d --scale worker=3
```

## 🤝 Contributing

### Development Workflow

1. Fork the repository
2. Create a feature branch
3. Make changes following code standards
4. Write/update tests
5. Ensure 80%+ test coverage
6. Submit pull request

### Code Review Checklist

- [ ] PEP 8 compliant
- [ ] Functions ≤ 14 lines
- [ ] Proper documentation
- [ ] Tests included
- [ ] No dead code
- [ ] Security considerations

## 📄 License

This project is part of the Developer Akademie curriculum.

## 📞 Support

For questions and support:
- Review the code documentation
- Check existing issues
- Create detailed bug reports
- Follow the contribution guidelines

---

**Built with ❤️ for Developer Akademie**

## Table of Contents

<!-- TOC -->

- [Videoflix - Docker Setup](#videoflix---docker-setup)
  - [Table of Contents](#table-of-contents)
  - [Voraussetzungen](#voraussetzungen)
  - [Quickstart](#quickstart)
    - [Aufsetzen und Einrichtung des Projekts](#aufsetzen-und-einrichtung-des-projekts)
      - [Anpassen der settings.py Datei](#anpassen-der-settingspy-datei)
  - [Usage](#usage)
    - [Environment Variablen](#environment-variablen)
    - [Migrations im Docker Container](#migrations-im-docker-container)
    - [requirements.txt](#requirementstxt)
  - [Troubleshooting](#troubleshooting)

<!-- /TOC -->

---

## Voraussetzungen

- **Docker** mit **docker-compose** installiert.

    Siehe [Anleitung](https://docs.docker.com/compose/install/) zur Installation.

    Erforderlich für den Start des Projekts, da es vollständig containerisiert ist.

- **git** ist installiert.

    Siehe [Anleitung](https://git-scm.com/downloads) zur Installation.

    Erforderlich, um das Projekt herunterzuladen.

---

## Quickstart

> [!CAUTION]
> <span style="color: red;">Bitte halte dich genau an die hier beschriebene Anleitung. Wenn du die grundlegene
Konfiguration veränderst, kann das Projekt unter Umständen nicht gestartet werden.</span>
>
> <span style="color: red;">Du kannst Variablen in der `.env` Datei verändern oder neue hinzufügen. Bitte lösche keine
der vorhandenen Variablen.</span>
>
> <span style="color: red;">Bitte ändere nichts, an den im weiteren Verlauf, angegebenen Einträgen in der `settings.py`.</span>
>
> <span style="color: red;">Bitte nimm keine Änderungen an den Dateien `backend.Dockerfile`, `docker-compose` und `backend.entrypoint.sh` vor!<ins></span>
>
> <span style="color: red;">Du kannst (und musst), weitere Packages installieren und auch entsprechende Änderungen an
der `settings.py` Datei vornehmen. <ins>Achte darauf deine `requirements.txt` Datei regelmäßig zu aktualisieren.<ins></span>

1. **Definiere die Umgebungsvariablen, unter Benutzung der [.env.template](./.env.template) Datei**. Nutze hierzu die
`git bash Komandozeile`.

    ```bash
    # Erstellt eine .env-Datei mit dem Inhalt von .env.template
    cp .env.template .env
    ```

    > [!IMPORTANT]
    > Stelle sicher, dass die Platzhalterwerte gegebenenfalls durch tatsächliche, für deine Umgebung spezifische Werte
    ersetzt werden.

### Aufsetzen und Einrichtung des Projekts

- Virtual Environment erstellen und aktivieren
- Django installieren
- DRF Installieren
- django rq installieren
- django-redis installieren
- gunicorn installieren
- psycopg2-binary installieren
- python-dotenv installieren
- whitenoise installieren
- aktualisiere deine `requirements.txt` Datei
- erstelle das Django Projekt im aktuellen Ordner
    - projektname => core

#### <ins>Anpassen der `settings.py` Datei

Passe deine `seetings.py` Datei wie folgt an (Bitte lösche unnötige Kommentare, die dir ggf. nur Informationen zum
Editieren liefern. Die ... geben an, dass hier weitere Zeilen stehen, diese müssen auch erhalten bleiben):

```python
# settings.py

from pathlib import Path
# zwei neue Zeilen
import os
from dotenv import load_dotenv

load_dotenv()
...

# folgende Zeile ändern
SECRET_KEY = os.getenv('SECRET_KEY', default='django-insecure-@#x5h3zj!g+8g1v@2^b6^9$8&f1r7g$@t3v!p4#=g0r5qzj4m3')

# Zwei Zeilen hinzufügen
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", default="localhost").split(",")
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", default="http://localhost:4200").split(",")

# Füge django-rq zu deinen Apps hinzu
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_rq', # neue Zeile
]

# Füge das whitenoise middleware hinzu
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # neue Zeile
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

...

# Ändere die Einstellungen für die Datenbak und Füge die Konfiguration für Redis und den RQ-Worker hinzu

# Ersetze die DATABASES Einstellung
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", default="videoflix_db"),
        "USER": os.environ.get("DB_USER", default="videoflix_user"),
        "PASSWORD": os.environ.get("DB_PASSWORD", default="supersecretpassword"),
        "HOST": os.environ.get("DB_HOST", default="db"),
        "PORT": os.environ.get("DB_PORT", default=5432)
    }
}

# Füge die Konfiguration für Redis und RQ hinzu
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_LOCATION", default="redis://redis:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "videoflix"
    }
}

RQ_QUEUES = {
    'default': {
        'HOST': os.environ.get("REDIS_HOST", default="redis"),
        'PORT': os.environ.get("REDIS_PORT", default=6379),
        'DB': os.environ.get("REDIS_DB", default=0),
        'DEFAULT_TIMEOUT': 900,
        'REDIS_CLIENT_KWARGS': {},
    },
}

...

# Ändere und Erweitere die Konfiguration für static und media Dateien
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

...

```

1. **Build and start the project using `docker-compose`.**

```bash
docker-compose up --build
```

-> falls das nicht funktioniert, verwende (ohne "-")
```bash
docker compose up --build
```

Open application in browser on [localhost:8000](http://localhost:8000).

---

## Usage

### Environment Variablen

Alle erforderlichen Umgebungsvariablen werden in der [.env](./.env) Datei gespeichert.

> [!IMPORTANT]
> Bitte verändere die Namen der Variablen in dieser Konfiguration nicht. Dies kann unter Umständen dazu führen, dass wir
das Projekt nicht prüfen und abnehmen können.
>
> Ändere bereits vorhandene Variablen gegebenenfalls mit sinnvollen Werten

---

> [!NOTE]
> [backend.entrypoint.sh](backend.entrypoint.sh) erstellt automatisch einen Superuser basierend auf den
Umgebungsvariablen **`DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_PASSWORD` und `DJANGO_SUPERUSER_EMAIL`**

| Name | Type | Description | Default | Mandatory |
| :--- | :---: | :---------- | :----- | :---: |
| **DJANGO_SUPERUSER_USERNAME** | str | Benutzername für das Django-Admin-Superuser-Konto. Dieser Benutzer wird automatisch erstellt wenn er nicht existiert. | `admin` |   |
| **DJANGO_SUPERUSER_PASSWORD** | str |  Passwort für das Django-Admin-Superuser-Konto. Achte darauf, dass es sicher ist. | `adminpassword` |   |
| **DJANGO_SUPERUSER_EMAIL** | str |  E-Mail-Adresse für das Django-Admin-Superuser-Konto. Wird für die Wiederherstellung des Kontos und für Benachrichtigungen verwendet. | `admin@example.com` |   |
| **SECRET_KEY** | str | Ein geheimer Schlüssel für die Kryptografie in Django. Dieser sollte eine lange, zufällige Zeichenfolge sein und vertraulich behandelt werden. |   | x |
| **DEBUG** | bool | Aktiviert oder deaktiviert den Debug-Modus. Sollte in der Produktion auf False gesetzt werden, um die Offenlegung sensibler Informationen zu verhindern. | `True` |   |
| **ALLOWED_HOSTS** | List[str] | Eine Liste von Strings, die die Host-/Domainnamen darstellen, die diese Django-Site bedienen kann. Wichtig für die Sicherheit. | `[localhost]` |   |
| **CSRF_TRUSTED_ORIGINS** | List[str] | Cors-Headers allowed origins. | `[http://localhost:4200]` |   |
| **DB_NAME** | str | Name der PostgreSQL-Datenbank, zu der eine Verbindung hergestellt werden soll. Wichtig für Datenbankoperationen. | `your_database_name` | x |
| **DB_USER** | str | Benutzername für die Authentifizierung bei der PostgreSQL-Datenbank. | `your_database_user` | x |
| **DB_PASSWORD** | str | Passwort für den PostgreSQL-Datenbankbenutzer. | `your_database_password` | x |
| **DB_HOST** | str | Host-Adresse der PostgreSQL-Datenbank. Normalerweise localhost oder der Dienstname in Docker. | `db` |   |
| **DB_PORT** | int | Portnummer für die Verbindung zur PostgreSQL-Datenbank. | `5432` |   |
| **REDIS_LOCATION** | str | Redis location | `redis://redis:6379/1` |   |
| **REDIS_HOST** | str | Redis host | `redis` |   |
| **REDIS_PORT** | int | Redis port | `6379` |   |
| **REDIS_DB** | int | Redis DB | `0` |   |
| **EMAIL_HOST** | str | SMTP-Server-Adresse für den Versand von E-Mails. | `smtp.example.com` | x |
| **EMAIL_PORT** | int | Portnummer für den SMTP-Server. | `587` |   |
| **EMAIL_USE_TLS** | bool | Aktiviert TLS für den E-Mail-Versand. Empfohlen für die Sicherheit. | `True` |   |
| **EMAIL_USE_SSL** | bool | E-Mail verwendet SSL | `False` |   |
| **EMAIL_HOST_USER** | str | Benutzername für das E-Mail-Konto, das zum Senden von E-Mails verwendet wird. | `your_email_user` | x |
| **EMAIL_HOST_PASSWORD** | str | Passwort für das E-Mail-Konto. Achte auf die Sicherheit. | `your_email_password` | x |
| **DEFAULT_FROM_EMAIL** | str | E-Mailadresse die von Django verwendet wird | `EMAIL_HOST_USER` |   |

### Migrations im Docker Container

Um gemachte Änderungen an der Datenbankstruktur an Docker zu übertragen hast du zwei verschiedene Möglichkeiten:

1. Docker Container komplett neu erstellen (nicht empfohlen)

    - stoppe Docker in der Kommandozeile mit der Tastenkombination `Strg+C`
    - starte Docker neu mit dem Befehl `docker-compose up --build`
    - falls `docker-compose up --build` nicht funktioniert, verwende `docker compose up --build`

2. Führe die Migration direkt im Docker Container aus (besser)

    - erstelle die migrations Dateien direkt im Docker Container

    ```bash
    docker-compose exec web python manage.py makemigrations
    ```

    Dieser Befehl wird direk in der Bash des Docker Containers ausgeführt. (Wir erinnern uns, unser Docker Setup
    enthält im Prinzip ein komplettes Betriebssystem)

    - Führe die Migration aus:

    ```bash
    docker-compose exec web python manage.py migrate
    ```

### requirements.txt

Die Dependencies der Anwendung sind in der Datei [requirements.txt](./requirements.txt) aufgeführt.

Um sie in den Docker Container zu ändern, muss die Anwendung neu erstellt werden.

Um nur die primären (Top-Level) Pakete aufzulisten, die du über `pip` installiert hast - ohne ihre Abhängigkeiten
anzuzeigen - verwende:

```bash
pip list --not-required
```

## Troubleshooting

- **Beim Starten von Docker erhalte ich in der Komandozeile diesen Fehler:**

    ```bash
    unable to get image 'postgres:latest': error during connect:
    Get "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/v1.48/images/postgres:latest/json":
    open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified.
    ```

    > [!NOTE]
    > Bitte stelle sicher, dass du Docker Desktop gestartet hast.

- **Das Starten von Docker bricht mit der folgenden Meldung in der Konsole ab:**

    ```bash
    videoflix_backend   | exec ./backend.entrypoint.sh: no such file or directory
    videoflix_backend exited with code 255
    ```

    > [!NOTE]
    > Bitte stelle sicher, dass die Datei `backend.entrypoint.sh` mit der End of Line Sequence LF abgespeichert ist.
    >
    > Siehe [Google Suche](https://www.google.com/search?sca_esv=81208bf63503b115&rlz=1C1CHBF_deDE1069DE1069&q=cr+lf+lf+in+vscode&spell=1&sa=X&ved=2ahUKEwihofbto4eNAxXK9bsIHXhtCLYQBSgAegQIDxAB&biw=1920&bih=911&dpr=1)

- **Beim Starten des Docker Containern erhältst du nach einer Änderung der Datenbank eine Fehlermeldung, dass die
Migration der Datenbank fehlschlägt.**

    > [!NOTE]
    > Dies kann passieren, wenn du Änderungen an einem Model vornimmst. Um trotzdem eine Migration durchführen zu können
    kannst do folgenden Befehl verwenden:
    >
    > ```bash
    > # docker run --rm [OPTIONEN] <DEIN_IMAGE_NAME> <DEIN_MIGRATIONSBEFEHL>
    > docker run --rm web python manage.py makemigrations
    >
    > # oftmals reicht dieser Befehl bereits aus um beim nächsten start das Problem zu umgehen.
    > # Zur Sicherheit kannst du aber auch direkt im Anschluss die eigentliche Migration durchführen.
    > docker run --rm web python manage.py migrate
    > ```
    >
---
