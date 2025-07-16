#!/usr/bin/env python3
"""
🎬 Videoflix Backend - Automatic Setup Script
============================================

This script checks the system and sets up the backend automatically.
It performs all necessary steps to make the project ready to run.
"""

import os
import sys
import subprocess
import time
import shutil
from pathlib import Path

# Colors for output
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

def run_command_with_retry(description, command, max_retries=3, retry_delay=2):
    """Executes commands with retry mechanism"""
    for attempt in range(max_retries):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            print_success(f"{description} - Successful")
            return result
        except subprocess.CalledProcessError as e:
            if attempt == max_retries - 1:
                print_error(f"{description} - Failed: {e.stderr}")
                raise
            else:
                print_warning(f"{description} - Attempt {attempt + 1} failed, retrying...")
                time.sleep(retry_delay)

def run_command(command, description, check_output=False):
    """Executes a command and returns the status"""
    print_info(f"Executing: {description}")
    try:
        if check_output:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print_success(f"{description} - Successful")
                return True, result.stdout
            else:
                print_error(f"{description} - Failed: {result.stderr}")
                return False, result.stderr
        else:
            result = subprocess.run(command, shell=True)
            if result.returncode == 0:
                print_success(f"{description} - Successful")
                return True, ""
            else:
                print_error(f"{description} - Failed")
                return False, ""
    except Exception as e:
        print_error(f"{description} - Error: {str(e)}")
        return False, str(e)

def check_requirements():
    """Checks system requirements"""
    print_header("🔍 CHECKING SYSTEM REQUIREMENTS")
    
    checks = [
        ("Check Docker version", "docker --version"),
        ("Check Docker Compose version", "docker-compose --version"),
        ("Check Python version", "python --version")
    ]
    
    for description, command in checks:
        success, output = run_command(command, description, check_output=True)
        if not success:
            if "docker" in command.lower():
                print_error("Docker is not installed or not available!")
                print_info("Please install Docker Desktop from: https://www.docker.com/products/docker-desktop")
            elif "python" in command.lower():
                print_error("Python is not installed!")
            return False
    
    print_success("All system requirements met!")
    return True

def setup_environment():
    """Sets up the environment automatically"""
    print_header("⚙️  SETTING UP ENVIRONMENT")
    
    # Automatic .env creation from template
    if not os.path.exists('.env'):
        if os.path.exists('.env.template'):
            shutil.copy('.env.template', '.env')
            print_success(".env file created from template")
        else:
            # Fallback: Create minimal .env
            env_content = """# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings
DB_NAME=videoflix_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# Email Settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Admin User Settings
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@test.com
ADMIN_PASSWORD=admin123456
"""
            with open('.env', 'w') as f:
                f.write(env_content)
            print_success("Standard .env file created")
    else:
        print_success(".env file already exists")
    
    # Create necessary directories
    os.makedirs('logs', exist_ok=True)
    print_success("Logs folder created")
    
    os.makedirs('media', exist_ok=True)
    os.makedirs('media/videos', exist_ok=True)
    os.makedirs('media/video_thumbnails', exist_ok=True)
    print_success("Media folders created")
    
    return True

def check_container_status():
    """Checks detailed container status"""
    print_info("Checking container status...")
    result = subprocess.run(
        ["docker-compose", "ps", "--format", "table"],
        capture_output=True, text=True
    )
    print_info("Container status:")
    print(result.stdout)

def build_containers():
    """Builds and starts Docker containers with extended health checks"""
    print_header("🐳 BUILDING DOCKER CONTAINERS")
    
    steps = [
        ("Stop old containers", "docker-compose down"),
        ("Build and start containers", "docker-compose up -d --build")
    ]
    
    for description, command in steps:
        success, output = run_command(command, description)
        if not success:
            print_error(f"Error executing: {description}")
            return False
    
    # Wait for container start with status monitoring
    print_info("Waiting for containers to start...")
    time.sleep(10)
    
    # Extended health checks
    max_retries = 12
    retry_delay = 5
    
    for attempt in range(max_retries):
        print_info(f"Health check attempt {attempt + 1}/{max_retries}")
        
        # PostgreSQL health check
        pg_result = subprocess.run(
            ["docker-compose", "exec", "-T", "db", "pg_isready", "-h", "localhost"],
            capture_output=True, text=True
        )
        
        # Redis health check
        redis_result = subprocess.run(
            ["docker-compose", "exec", "-T", "redis", "redis-cli", "ping"],
            capture_output=True, text=True
        )
        
        if pg_result.returncode == 0 and redis_result.returncode == 0:
            print_success("All services are ready!")
            check_container_status()
            return True
        
        if attempt < max_retries - 1:
            print_warning(f"Services not ready yet, waiting {retry_delay} seconds...")
            time.sleep(retry_delay)
    
    print_error("Container startup failed after multiple attempts")
    check_container_status()
    return False

def setup_database():
    """Sets up the database automatically"""
    print_header("🗄️  SETTING UP DATABASE")
    
    steps = [
        ("Create migrations", "docker-compose exec -T web python manage.py makemigrations"),
        ("Migrate database", "docker-compose exec -T web python manage.py migrate")
    ]
    
    for description, command in steps:
        try:
            result = run_command_with_retry(description, command, max_retries=2, retry_delay=5)
            if description == "Create migrations" and "No changes detected" in result.stdout:
                print_info("No new migrations required")
        except subprocess.CalledProcessError as e:
            if description == "Create migrations":
                print_warning("Migrations could not be created - possibly already exist")
            else:
                print_error(f"Database migration failed: {e}")
                return False
    
    return True

def create_admin_user():
    """Creates and verifies admin user automatically"""
    print_header("👤 CREATING ADMIN USER")
    
    steps = [
        ("Create admin user", "docker-compose exec -T web python create_admin.py"),
        ("Verify admin user", "docker-compose exec -T web python verify_admin.py")
    ]
    
    for description, command in steps:
        try:
            result = run_command_with_retry(description, command, max_retries=2, retry_delay=3)
        except subprocess.CalledProcessError as e:
            print_warning(f"{description} - Possibly already exists or other condition met")
            continue
    
    return True

def run_tests():
    """Runs automatic tests"""
    print_header("🧪 RUNNING TESTS")
    
    steps = [
        ("Run authentication tests", "docker-compose exec -T web python manage.py test authentication")
    ]
    
    for description, command in steps:
        try:
            result = run_command_with_retry(description, command, max_retries=1, retry_delay=2)
            print_success("Tests completed successfully")
        except subprocess.CalledProcessError as e:
            print_warning("Some tests failed, setup will continue")
            continue
    
    return True

def print_section(title):
    """Prints formatted section header"""
    print("=" * 60)
    print(f"{title}")
    print("=" * 60)

def print_success_message():
    """Prints final success message"""
    print_section("🎉 SETUP COMPLETED")
    print("✅ Backend is ready!")
    print()
    print("📋 IMPORTANT INFORMATION:")
    print("  • Backend URL: http://localhost:8000")
    print("  • Admin Panel: http://localhost:8000/admin")
    print("  • API Documentation: http://localhost:8000/api/")
    print()
    print("🔑 ADMIN LOGIN CREDENTIALS:")
    print("  • Email: admin@test.com")
    print("  • Password: admin123456")
    print("  • Username: admin")

def print_final_info():
    """Prints final information"""
    print_header("🎉 SETUP COMPLETED")
    
    print_success("Backend is ready!")
    print("")
    print(f"{Colors.BOLD}📋 IMPORTANT INFORMATION:{Colors.END}")
    print(f"  • Backend URL: http://localhost:8000")
    print(f"  • Admin Panel: http://localhost:8000/admin")
    print(f"  • API Documentation: http://localhost:8000/api/")
    print("")
    print(f"{Colors.BOLD}🔑 ADMIN LOGIN CREDENTIALS:{Colors.END}")
    print(f"  • Email: admin@test.com")
    print(f"  • Password: admin123456")
    print(f"  • Username: admin")
    print("")
    print(f"{Colors.BOLD}🐳 DOCKER COMMANDS:{Colors.END}")
    print(f"  • Stop containers: docker-compose down")
    print(f"  • Start containers: docker-compose up -d")
    print(f"  • View logs: docker-compose logs -f")
    print("")
    print(f"{Colors.BOLD}🛠️  USEFUL COMMANDS:{Colors.END}")
    print(f"  • Open shell: docker-compose exec web python manage.py shell")
    print(f"  • Run tests: docker-compose exec web python manage.py test")
    print(f"  • Create new admin: docker-compose exec web python create_admin.py")

def main():
    """Main function"""
    print_header("🎬 VIDEOFLIX BACKEND SETUP")
    print("This script sets up the backend automatically.")
    print("Please make sure Docker Desktop is running.")
    
    # Confirmation
    response = input(f"\n{Colors.YELLOW}Do you want to continue with the setup? (y/n): {Colors.END}")
    if response.lower() not in ['y', 'yes', 'j', 'ja']:
        print("Setup cancelled.")
        return
    
    try:
        # Execute steps
        if not check_requirements():
            return
        
        if not setup_environment():
            return
        
        if not build_containers():
            return
        
        if not setup_database():
            return
        
        if not create_admin_user():
            return
        
        run_tests()
        
        print_final_info()
        
    except KeyboardInterrupt:
        print_error("\nSetup was interrupted.")
        print_info("Containers can be stopped with 'docker-compose down'.")
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
