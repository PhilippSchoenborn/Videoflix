#!/usr/bin/env python3
"""
🎬 Videoflix Backend - Fixed Automatic Setup Script
==================================================

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

def run_command(command, description, check_return_code=True):
    """Runs a shell command and returns success status and output"""
    print_info(f"{description}...")
    try:
        result = subprocess.run(
            command.split() if isinstance(command, str) else command,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if check_return_code and result.returncode != 0:
            print_error(f"Command failed: {command}")
            print_error(f"Error output: {result.stderr}")
            return False, result.stderr
        
        return True, result.stdout
    except subprocess.TimeoutExpired:
        print_error(f"Command timed out: {command}")
        return False, "Command timed out"
    except Exception as e:
        print_error(f"Command execution failed: {e}")
        return False, str(e)

def check_system_requirements():
    """Checks if all required tools are installed"""
    print_header("🔍 CHECKING SYSTEM REQUIREMENTS")
    
    requirements = [
        ("docker", "Docker"),
        ("docker-compose", "Docker Compose")
    ]
    
    for command, name in requirements:
        try:
            result = subprocess.run([command, "--version"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print_success(f"{name} is installed")
            else:
                print_error(f"{name} is not working properly")
                return False
        except FileNotFoundError:
            print_error(f"{name} is not installed")
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
            print_error(".env.template not found!")
            return False
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

def clean_old_migrations():
    """Clean problematic old migrations"""
    print_info("Cleaning old migrations...")
    
    migration_dirs = [
        "authentication/migrations",
        "videos/migrations", 
        "utils/migrations",
        "content/migrations"
    ]
    
    for migration_dir in migration_dirs:
        if os.path.exists(migration_dir):
            # Keep only __init__.py and 0001_initial.py if they exist
            for file in os.listdir(migration_dir):
                if file.endswith('.py') and file not in ['__init__.py', '0001_initial.py']:
                    file_path = os.path.join(migration_dir, file)
                    try:
                        os.remove(file_path)
                        print_info(f"Removed migration: {file}")
                    except Exception as e:
                        print_warning(f"Could not remove {file}: {e}")
    
    print_success("Migration cleanup completed")

def build_containers():
    """Builds and starts Docker containers with robust health checks"""
    print_header("🐳 BUILDING DOCKER CONTAINERS")
    
    # Step 1: Clean up
    print_info("Cleaning up old containers and volumes...")
    cleanup_commands = [
        "docker-compose down -v",
        "docker system prune -f"
    ]
    
    for cmd in cleanup_commands:
        subprocess.run(cmd.split(), capture_output=True)
    
    # Step 2: Clean migrations
    clean_old_migrations()
    
    # Step 3: Build containers
    success, output = run_command("docker-compose build --no-cache", "Building containers")
    if not success:
        print_error("Failed to build containers")
        return False
    
    # Step 4: Start containers  
    success, output = run_command("docker-compose up -d", "Starting containers")
    if not success:
        print_error("Failed to start containers")
        return False
    
    # Step 5: Wait and health check
    print_info("Waiting for services to be healthy...")
    
    max_retries = 24  # 2 minutes total
    retry_delay = 5
    
    for attempt in range(max_retries):
        print_info(f"Health check attempt {attempt + 1}/{max_retries}")
        
        all_healthy = True
        services_status = {}
        
        # Check PostgreSQL
        try:
            pg_result = subprocess.run(
                ["docker-compose", "exec", "-T", "db", "pg_isready", "-U", "postgres"],
                capture_output=True, text=True, timeout=10
            )
            if pg_result.returncode == 0:
                services_status['postgresql'] = True
                print_success("PostgreSQL is healthy")
            else:
                services_status['postgresql'] = False
                print_info("PostgreSQL not ready yet...")
                all_healthy = False
        except Exception:
            services_status['postgresql'] = False
            all_healthy = False
        
        # Check Redis
        try:
            redis_result = subprocess.run(
                ["docker-compose", "exec", "-T", "redis", "redis-cli", "ping"],
                capture_output=True, text=True, timeout=10
            )
            if redis_result.returncode == 0 and "PONG" in redis_result.stdout:
                services_status['redis'] = True
                print_success("Redis is healthy")
            else:
                services_status['redis'] = False
                print_info("Redis not ready yet...")
                all_healthy = False
        except Exception:
            services_status['redis'] = False
            all_healthy = False
        
        # Check Web service
        try:
            web_result = subprocess.run(
                ["docker-compose", "exec", "-T", "web", "python", "manage.py", "check", "--deploy"],
                capture_output=True, text=True, timeout=15
            )
            if web_result.returncode == 0:
                services_status['web'] = True
                print_success("Web service is healthy")
            else:
                services_status['web'] = False
                print_info("Web service not ready yet...")
                all_healthy = False
        except Exception:
            services_status['web'] = False
            all_healthy = False
        
        if all_healthy:
            print_success("All services are healthy!")
            break
            
        if attempt < max_retries - 1:
            print_info(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
    else:
        print_error("Services did not become healthy within timeout")
        print_info("Showing container status and logs:")
        subprocess.run(["docker-compose", "ps"])
        subprocess.run(["docker-compose", "logs", "--tail=20"])
        return False
    
    return True

def setup_database():
    """Sets up the database with migrations"""
    print_header("🗄️  SETTING UP DATABASE")
    
    commands = [
        ("python manage.py makemigrations", "Creating migrations"),
        ("python manage.py migrate", "Running migrations"),
    ]
    
    for command, description in commands:
        success, output = run_command(
            f"docker-compose exec -T web {command}",
            description
        )
        if not success:
            print_error(f"Database setup failed: {description}")
            print_error(f"Output: {output}")
            return False
    
    print_success("Database setup completed!")
    return True

def create_admin_user():
    """Creates admin user"""
    print_header("👤 CREATING ADMIN USER")
    
    success, output = run_command(
        "docker-compose exec -T web python create_admin.py",
        "Creating admin user"
    )
    
    if success:
        print_success("Admin user created successfully!")
        print_info("Login credentials:")
        print_info("  Email: admin@test.com")
        print_info("  Password: admin123456")
        return True
    else:
        print_warning("Admin user creation failed (may already exist)")
        return True  # Not critical failure

def run_tests():
    """Runs the test suite"""
    print_header("🧪 RUNNING TESTS")
    
    success, output = run_command(
        "docker-compose exec -T web python manage.py test --verbosity=2",
        "Running test suite"
    )
    
    if success:
        print_success("All tests passed!")
    else:
        print_warning("Some tests failed (not critical for setup)")
        print_info("You can run tests manually later with: docker-compose exec web python manage.py test")
    
    return True

def show_final_info():
    """Shows final setup information"""
    print_header("🎉 SETUP COMPLETED!")
    
    print_success("Videoflix Backend is ready!")
    print_info("\n📋 QUICK ACCESS:")
    print_info("  🌐 Backend API: http://localhost:8000")
    print_info("  🔧 Admin Panel: http://localhost:8000/admin")
    print_info("  📧 Admin Login: admin@test.com / admin123456")
    
    print_info("\n🚀 USEFUL COMMANDS:")
    print_info("  📊 View logs: docker-compose logs")
    print_info("  🔄 Restart: docker-compose restart")
    print_info("  🛑 Stop: docker-compose down")
    print_info("  🧪 Run tests: docker-compose exec web python manage.py test")
    
    print_info("\n📧 EMAIL SETUP (Optional):")
    print_info("  📝 Edit .env file with your Gmail credentials")
    print_info("  📖 See README.md for detailed instructions")

def main():
    """Main setup function"""
    print_header("🎬 VIDEOFLIX BACKEND SETUP")
    print_info("Starting automatic setup process...")
    
    steps = [
        ("Checking system requirements", check_system_requirements),
        ("Setting up environment", setup_environment),
        ("Building containers", build_containers),
        ("Setting up database", setup_database),
        ("Creating admin user", create_admin_user),
        ("Running tests", run_tests),
    ]
    
    for step_name, step_function in steps:
        print_info(f"\n🔄 {step_name}...")
        if not step_function():
            print_error(f"Setup failed at step: {step_name}")
            print_error("Please check the error messages above and try again.")
            return False
    
    show_final_info()
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print_error("\nSetup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
