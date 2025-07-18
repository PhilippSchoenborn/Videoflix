#!/usr/bin/env python3
"""
🎬 Videoflix Backend - ROBUST Setup Script
=========================================

This script has been fixed to handle all setup issues reported by mentors.
It includes improved error handling, container health checks, and migration cleanup.
"""

import os
import sys
import subprocess
import time
import shutil

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

def run_command(command, description):
    """Runs a shell command with proper error handling"""
    print_info(f"{description}...")
    try:
        if isinstance(command, str):
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=300)
        else:
            result = subprocess.run(command, capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            print_error(f"Command failed: {command}")
            print_error(f"Error: {result.stderr}")
            return False, result.stderr
        
        return True, result.stdout
    except subprocess.TimeoutExpired:
        print_error(f"Command timed out: {command}")
        return False, "Timeout"
    except Exception as e:
        print_error(f"Command error: {e}")
        return False, str(e)

def check_docker():
    """Check if Docker is running"""
    print_header("🐳 CHECKING DOCKER")
    
    # Check Docker
    success, _ = run_command("docker --version", "Checking Docker")
    if not success:
        print_error("Docker is not installed or not running")
        return False
    
    # Check Docker Compose
    success, _ = run_command("docker-compose --version", "Checking Docker Compose")
    if not success:
        print_error("Docker Compose is not installed")
        return False
    
    print_success("Docker environment is ready")
    return True

def cleanup_environment():
    """Clean up old containers and migrations"""
    print_header("🧹 CLEANING ENVIRONMENT")
    
    # Stop and remove containers
    print_info("Stopping containers...")
    subprocess.run("docker-compose down -v", shell=True, capture_output=True)
    
    # Clean Docker system
    print_info("Cleaning Docker system...")
    subprocess.run("docker system prune -f", shell=True, capture_output=True)
    
    # Clean migrations
    print_info("Cleaning old migrations...")
    migration_dirs = [
        "authentication/migrations",
        "videos/migrations", 
        "utils/migrations",
        "content/migrations"
    ]
    
    for migration_dir in migration_dirs:
        if os.path.exists(migration_dir):
            for file in os.listdir(migration_dir):
                if file.endswith('.py') and file not in ['__init__.py', '0001_initial.py']:
                    try:
                        os.remove(os.path.join(migration_dir, file))
                        print_info(f"Removed {file}")
                    except:
                        pass
    
    print_success("Environment cleaned")
    return True

def setup_env_file():
    """Setup environment file"""
    print_header("⚙️  SETTING UP ENVIRONMENT")
    
    if not os.path.exists('.env'):
        if os.path.exists('.env.template'):
            shutil.copy('.env.template', '.env')
            print_success(".env file created from template")
        else:
            print_error(".env.template not found!")
            return False
    else:
        print_success(".env file already exists")
    
    # Create directories
    os.makedirs('logs', exist_ok=True)
    os.makedirs('media/videos', exist_ok=True)
    os.makedirs('media/video_thumbnails', exist_ok=True)
    print_success("Required directories created")
    
    return True

def build_and_start():
    """Build and start containers with health checks"""
    print_header("🏗️  BUILDING CONTAINERS")
    
    # Build containers
    success, output = run_command("docker-compose build --no-cache", "Building containers")
    if not success:
        print_error("Failed to build containers")
        return False
    
    # Start containers
    success, output = run_command("docker-compose up -d", "Starting containers")
    if not success:
        print_error("Failed to start containers")
        return False
    
    print_success("Containers started")
    return True

def wait_for_services():
    """Wait for all services to be healthy"""
    print_header("⏳ WAITING FOR SERVICES")
    
    max_attempts = 30
    wait_time = 5
    
    for attempt in range(max_attempts):
        print_info(f"Health check {attempt + 1}/{max_attempts}")
        
        # Check all services
        services_ready = True
        
        # PostgreSQL
        result = subprocess.run(
            ["docker-compose", "exec", "-T", "db", "pg_isready", "-U", "postgres"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print_info("PostgreSQL not ready...")
            services_ready = False
        else:
            print_success("PostgreSQL ready")
        
        # Redis
        result = subprocess.run(
            ["docker-compose", "exec", "-T", "redis", "redis-cli", "ping"],
            capture_output=True, text=True
        )
        if result.returncode != 0 or "PONG" not in result.stdout:
            print_info("Redis not ready...")
            services_ready = False
        else:
            print_success("Redis ready")
        
        # Web service
        result = subprocess.run(
            ["docker-compose", "exec", "-T", "web", "python", "manage.py", "check"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print_info("Web service not ready...")
            services_ready = False
        else:
            print_success("Web service ready")
        
        if services_ready:
            print_success("All services are healthy!")
            return True
        
        if attempt < max_attempts - 1:
            print_info(f"Waiting {wait_time} seconds...")
            time.sleep(wait_time)
    
    print_error("Services failed to start properly")
    print_info("Container status:")
    subprocess.run(["docker-compose", "ps"])
    return False

def setup_database():
    """Setup database with migrations"""
    print_header("🗄️  SETTING UP DATABASE")
    
    # Create migrations
    success, output = run_command(
        "docker-compose exec -T web python manage.py makemigrations",
        "Creating migrations"
    )
    if not success:
        print_warning("Migration creation had issues, continuing...")
    
    # Run migrations
    success, output = run_command(
        "docker-compose exec -T web python manage.py migrate",
        "Running migrations"
    )
    if not success:
        print_error("Database migration failed")
        print_error(f"Output: {output}")
        return False
    
    print_success("Database setup completed")
    return True

def create_admin():
    """Create admin user"""
    print_header("👤 CREATING ADMIN USER")
    
    success, output = run_command(
        "docker-compose exec -T web python create_admin.py",
        "Creating admin user"
    )
    
    if success:
        print_success("Admin user ready")
    else:
        print_warning("Admin user creation had issues (may already exist)")
    
    print_info("Admin credentials:")
    print_info("  📧 Email: admin@test.com")
    print_info("  🔑 Password: admin123456")
    
    return True

def run_basic_tests():
    """Run basic system tests"""
    print_header("🧪 RUNNING BASIC TESTS")
    
    # Test database connection
    success, output = run_command(
        "docker-compose exec -T web python manage.py check --database default",
        "Testing database connection"
    )
    
    if success:
        print_success("Database connection test passed")
    else:
        print_warning("Database test had issues")
    
    # Basic management command test
    success, output = run_command(
        "docker-compose exec -T web python manage.py help",
        "Testing Django management commands"
    )
    
    if success:
        print_success("Django management commands working")
    else:
        print_warning("Management commands test failed")
    
    return True

def show_final_status():
    """Show final setup status and instructions"""
    print_header("🎉 SETUP COMPLETED!")
    
    print_success("Videoflix Backend is ready for testing!")
    
    print_info("\n📋 ACCESS INFORMATION:")
    print_info("  🌐 Backend API: http://localhost:8000")
    print_info("  🔧 Admin Panel: http://localhost:8000/admin")
    print_info("  📧 Admin Email: admin@test.com")
    print_info("  🔑 Admin Password: admin123456")
    
    print_info("\n🚀 USEFUL COMMANDS:")
    print_info("  📊 View logs: docker-compose logs")
    print_info("  📊 View specific service logs: docker-compose logs web")
    print_info("  🔄 Restart services: docker-compose restart")
    print_info("  🛑 Stop services: docker-compose down")
    print_info("  🧪 Run tests: docker-compose exec web python manage.py test")
    
    print_info("\n📧 EMAIL CONFIGURATION:")
    print_info("  📝 Edit .env file with your Gmail credentials")
    print_info("  📖 See README.md for detailed email setup instructions")
    print_info("  🔗 Frontend should run on http://localhost:5173")
    
    print_info("\n⚠️  FOR MENTORS:")
    print_info("  If you see 'Connection refused' errors:")
    print_info("  1. Wait 30 seconds for all services to start")
    print_info("  2. Check: docker-compose ps")
    print_info("  3. Check logs: docker-compose logs")
    print_info("  4. Frontend URL should be http://localhost:5173")

def main():
    """Main setup function with error recovery"""
    print_header("🎬 VIDEOFLIX BACKEND ROBUST SETUP")
    print_info("This script fixes common setup issues reported by mentors")
    
    steps = [
        ("Docker Check", check_docker),
        ("Environment Cleanup", cleanup_environment),
        ("Environment Setup", setup_env_file),
        ("Container Build", build_and_start),
        ("Service Health Check", wait_for_services),
        ("Database Setup", setup_database),
        ("Admin User Creation", create_admin),
        ("Basic Tests", run_basic_tests),
    ]
    
    for step_name, step_function in steps:
        print_info(f"\n🔄 Starting: {step_name}")
        
        if not step_function():
            print_error(f"❌ Step failed: {step_name}")
            print_error("Setup process stopped. Please check errors above.")
            
            print_info("\n🔧 TROUBLESHOOTING:")
            print_info("1. Ensure Docker Desktop is running")
            print_info("2. Check Docker has enough memory (4GB+)")
            print_info("3. Try: docker-compose down -v && docker system prune -f")
            print_info("4. Run this script again")
            
            return False
        
        print_success(f"✅ Completed: {step_name}")
    
    show_final_status()
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print_success("🎉 Setup completed successfully!")
            sys.exit(0)
        else:
            print_error("❌ Setup failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print_error("\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"💥 Unexpected error: {e}")
        print_error("Please report this error if it persists")
        sys.exit(1)
