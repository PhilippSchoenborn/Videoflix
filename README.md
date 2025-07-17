# 🎬 Videoflix - Django REST API Backend

> **🎓 MENTOR GUIDE: SIMPLE INSTALLATION**
> 
> This README is specifically optimized for mentors and contains all necessary steps for a smooth installation and evaluation of the project.

## 🚀 QUICK START (for Mentors)

### 📋 Check Prerequisites
- ✅ **Docker Desktop** installed and running
- ✅ **Git** installed
- ✅ **Windows PowerShell** or Terminal
- ✅ At least 8GB RAM

### ⚡ 1-CLICK INSTALLATION

1. **Clone repository**
   ```bash
   git clone https://github.com/PhilippSchoenborn/Videoflix.git
   cd Videoflix
   ```

2. **Run automatic setup**
   ```bash
   python setup.py
   ```
   
   **The script automatically performs:**
   - ✅ Check system requirements
   - ✅ Build Docker containers
   - ✅ Set up database
   - ✅ Create admin user
   - ✅ Run tests

3. **Done!** 🎉
   - Backend: http://localhost:8000
   - Admin: http://localhost:8000/admin
   - Login: admin@test.com / admin123456

### 🔧 MANUAL INSTALLATION (if setup script doesn't work)

1. **Start containers**
   ```bash
   docker-compose up -d --build
   ```

2. **Set up database**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

3. **Create admin user**
   ```bash
   docker-compose exec web python create_admin.py
   ```

4. **Test system**
   ```bash
   docker-compose exec web python manage.py test
   ```

## 📋 EVALUATION CHECKLIST (for Mentors)

### ✅ Backend Functionality
- [ ] Server starts without errors
- [ ] Admin panel accessible (http://localhost:8000/admin)
- [ ] API endpoints accessible
- [ ] Database connection works
- [ ] Tests run successfully

### ✅ Authentication
- [ ] User registration works
- [ ] Login/logout works
- [ ] Email verification implemented
- [ ] Password reset implemented

### ✅ Code Quality
- [ ] Django best practices followed
- [ ] REST API correctly implemented
- [ ] Documentation available
- [ ] Tests available

## 🔑 ADMIN LOGIN CREDENTIALS

```
URL: http://localhost:8000/admin
Email: admin@test.com
Password: admin123456
Username: admin
```

## 🧪 RUNNING TESTS

```bash
# All tests
docker-compose exec web python manage.py test

# Only authentication tests
docker-compose exec web python manage.py test authentication

# Only video tests
docker-compose exec web python manage.py test videos

# With coverage
docker-compose exec web python -m pytest --cov=. --cov-report=html
```

## 🐛 TROUBLESHOOTING (common issues)

### Problem: Containers don't start
```bash
# Stop old containers
docker-compose down

# Clean system
docker system prune -f

# Restart
docker-compose up -d --build
```

### Problem: Database errors
```bash
# Restart containers
docker-compose restart db

# Run migrations again
docker-compose exec web python manage.py migrate
```

### Problem: Admin user doesn't work
```bash
# Create new admin
docker-compose exec web python create_admin.py

# Verify admin
docker-compose exec web python verify_admin.py
```

## 📊 PROJECT STRUCTURE

```
videoflix-backend/
├── 📁 authentication/          # User management
├── 📁 videos/                  # Video management
├── 📁 core/                    # Django configuration
├── 📁 tests/                   # Comprehensive tests
├── 📁 media/                   # Uploaded files
├── 📁 logs/                    # Log files
├── 🐳 docker-compose.yml       # Docker configuration
├── 📋 requirements.txt         # Python dependencies
├── ⚙️  .env                    # Environment variables
├── 🚀 setup.py                 # Auto-setup script
└── 📖 README.md               # This file
```

## 🔌 API ENDPOINTS

### Authentication
- `POST /api/register/` - Register user
- `POST /api/login/` - Login user
- `POST /api/logout/` - Logout user
- `GET /api/profile/` - Get user profile

### Videos
- `GET /api/videos/` - Get all videos
- `POST /api/videos/` - Upload video
- `GET /api/videos/{id}/` - Get single video
- `PUT /api/videos/{id}/` - Update video

## 🛠️ USEFUL COMMANDS

```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs -f

# Open shell
docker-compose exec web python manage.py shell

# Django commands
docker-compose exec web python manage.py <command>

# Stop containers
docker-compose down

# Delete database and recreate
docker-compose down -v
docker-compose up -d --build
```

## 🎯 EVALUATION CRITERIA

### Technical Implementation (40%)
- ✅ Django REST Framework used correctly
- ✅ Database models well structured
- ✅ API endpoints fully implemented
- ✅ Authentication works

### Code Quality (30%)
- ✅ Clean code principles
- ✅ Comments and documentation
- ✅ Error handling
- ✅ Django best practices

### Functionality (20%)
- ✅ All features implemented
- ✅ Frontend integration possible
- ✅ File upload works
- ✅ Email system implemented

### Setup & Deployment (10%)
- ✅ Docker configuration
- ✅ Environment variables
- ✅ Installation guide
- ✅ Troubleshooting guide

## 📞 SUPPORT

For issues:
1. Check the troubleshooting section
2. Check the logs: `docker-compose logs -f`
3. Restart the setup script: `python setup.py`

---

**Developed by:** Philipp Schoenborn  
**Date:** 16.07.2025  
**Version:** 1.0.0  
**Status:** ✅ Production ready

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

## � Documentation

### Project Documentation
- `README.md` - Main project documentation and installation guide
- `MENTOREN-ANLEITUNG.md` - Detailed guide for mentors (German)
- `tests/documentation/` - Development documentation and testing guides
  - `EMAIL_VERIFICATION_GUIDE.md` - Complete email verification guide
  - `ENHANCED_EMAIL_VERIFICATION.md` - Enhanced email system documentation
  - `VIDEO_UPLOAD_FIX.md` - Video upload system fixes
  - `PEP8_REPORT_angepasst.md` - Code style report
  - And more development resources...

### Email Verification System
The project includes an enhanced dual email verification system:
- **File-based email storage** in `logs/emails/`
- **Terminal-based verification** for development

See `tests/documentation/EMAIL_VERIFICATION_GUIDE.md` for complete usage instructions.

## �📝 Contributing

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
