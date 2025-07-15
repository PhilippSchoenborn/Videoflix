
# 🎬 Videoflix - Django REST API Backend

A modern video streaming backend API built with Django REST Framework.

## 🚀 Quick Start

### Prerequisites
- Docker Desktop (with docker-compose)
- Git
- 8GB+ RAM recommended

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd videoflix-backend
   ```

2. **Environment Configuration**
   ```bash
   cp .env.template .env
   # Edit .env file with your settings (database, email, etc.)
   ```

3. **Start the Application**
   ```bash
   # Build and start all services
   docker-compose up --build

   # Or run in background
   docker-compose up -d --build
   ```

4. **Database Setup**
   ```bash
   # Run migrations
   docker-compose exec web python manage.py migrate

   # Create superuser account
   docker-compose exec web python manage.py createsuperuser
   ```

5. **Access the Application**
   - **Backend API:** http://localhost:8000
   - **Django Admin:** http://localhost:8000/admin
   - **API Documentation:** http://localhost:8000/api/

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
- `GET /api/videos/<id>/` - Get specific video
- `GET /api/videos/<id>/stream/<resolution>/` - Stream video
- `GET /api/videos/featured/` - Get featured videos
- `GET /api/videos/by-genre/` - Get videos by genre
- `POST /api/videos/<id>/watch-progress/` - Update watch progress
- `GET /api/videos/continue-watching/` - Get continue watching list

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
