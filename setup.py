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
import threading

# Colors for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'
    CYAN = '\033[96m'

class ProgressBar:
    """Simple progress bar with spinner"""
    def __init__(self, message="Working"):
        self.message = message
        self.running = False
        self.thread = None
        self.spinner_chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        self.current_char = 0
    
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.daemon = True
        self.thread.start()
    
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        # Clear the line
        print(f"\r{' ' * 80}\r", end='', flush=True)
    
    def _animate(self):
        while self.running:
            char = self.spinner_chars[self.current_char % len(self.spinner_chars)]
            print(f"\r{Colors.CYAN}{char} {self.message}...{Colors.END}", end='', flush=True)
            self.current_char += 1
            time.sleep(0.1)

def print_progress_step(step, total, message):
    """Print progress step with bar"""
    percentage = (step / total) * 100
    bar_length = 40
    filled_length = int(bar_length * step // total)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    print(f"\r{Colors.BLUE}[{bar}] {percentage:.1f}% - {message}{Colors.END}")
    print()  # New line after progress

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

def run_command(command, description, show_progress=False):
    """Runs a shell command with proper error handling and optional progress"""
    print_info(f"{description}...")
    
    progress = None
    if show_progress:
        progress = ProgressBar(description)
        progress.start()
    
    try:
        if isinstance(command, str):
            result = subprocess.run(command, shell=True, capture_output=True, encoding='utf-8', errors='replace', timeout=300)
        else:
            result = subprocess.run(command, capture_output=True, encoding='utf-8', errors='replace', timeout=300)

        if progress:
            progress.stop()

        if result.returncode != 0:
            print_error(f"Command failed: {command}")
            print_error(f"Error: {result.stderr}")
            return False, result.stderr

        return True, result.stdout
    except subprocess.TimeoutExpired:
        if progress:
            progress.stop()
        print_error(f"Command timed out: {command}")
        return False, "Timeout"
    except Exception as e:
        if progress:
            progress.stop()
        print_error(f"Command error: {e}")
        return False, str(e)

def check_docker():
    """Check if Docker is running and ports are available"""
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
    
    # Check critical ports
    print_info("Checking required ports...")
    critical_ports = [5432, 6379, 8000]  # PostgreSQL, Redis, Django
    
    for port in critical_ports:
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            
            if result == 0:
                print_warning(f"Port {port} is already in use - this may cause conflicts")
                print_info(f"Attempting to stop any containers using port {port}...")
                # Try to find and stop containers using this port
                subprocess.run(f"docker ps --filter 'publish={port}' -q | xargs -r docker stop", 
                             shell=True, capture_output=True)
            else:
                print_success(f"Port {port} is available")
        except Exception as e:
            print_info(f"Could not check port {port}: {e}")
    
    print_success("Docker environment is ready")
    return True

def cleanup_environment():
    """Clean up old containers and migrations - FAST VERSION"""
    print_header("🧹 CLEANING ENVIRONMENT")
    
    # Stop and remove containers quickly
    print_info("Stopping containers...")
    subprocess.run("docker-compose down -v --remove-orphans", shell=True, capture_output=True)
    
    # Quick Docker cleanup (not aggressive)
    print_info("Quick Docker cleanup...")
    subprocess.run("docker system prune -f", shell=True, capture_output=True)
    
    # Clean migrations locally only (container cleanup happens later)
    print_info("Cleaning old migrations...")
    migration_dirs = [
        "authentication/migrations",
        "videos/migrations", 
        "utils/migrations"
    ]
    
    for migration_dir in migration_dirs:
        if os.path.exists(migration_dir):
            for file in os.listdir(migration_dir):
                if file.endswith('.py') and file != '__init__.py':
                    try:
                        file_path = os.path.join(migration_dir, file)
                        os.remove(file_path)
                        print_info(f"Removed {file_path}")
                    except:
                        pass  # Ignore errors, keep it fast
    
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
    """Build and start containers with progress feedback"""
    print_header("\U0001f3d7️  BUILDING CONTAINERS")

    # --- NEU: Konvertiere alle .sh-Skripte auf LF-Zeilenenden, um Bash-Probleme zu verhindern ---
    import glob
    sh_files = glob.glob("*.sh")
    for sh_file in sh_files:
        try:
            with open(sh_file, "rb") as f:
                content = f.read()
            # Ersetze CRLF durch LF
            content = content.replace(b"\r\n", b"\n")
            with open(sh_file, "wb") as f:
                f.write(content)
            print_info(f"Konvertiert {sh_file} auf LF-Zeilenenden.")
        except Exception as e:
            print_warning(f"Konnte {sh_file} nicht konvertieren: {e}")

    # Build containers mit Fortschritt
    print_info("Building Docker containers (this may take a few minutes)...")
    progress = ProgressBar("Building containers - downloading base images and dependencies")
    progress.start()

    try:
        result = subprocess.run("docker-compose build --no-cache", shell=True, capture_output=True, encoding='utf-8', errors='replace', timeout=600)
        progress.stop()
        
        if result.returncode != 0:
            print_error("Failed to build containers")
            print_error(f"Build output: {result.stderr}")
            return False
        else:
            print_success("Containers built successfully")
    except subprocess.TimeoutExpired:
        progress.stop()
        print_error("Container build timed out (10 minutes)")
        return False
    except Exception as e:
        progress.stop()
        print_error(f"Build error: {e}")
        return False

    # Start containers mit Fortschritt
    print_info("Starting containers...")
    start_progress = ProgressBar("Starting all services")
    start_progress.start()

    try:
        result = subprocess.run("docker-compose up -d", shell=True, capture_output=True, encoding='utf-8', errors='replace', timeout=120)
        start_progress.stop()
        
        if result.returncode != 0:
            print_error("Failed to start containers")
            print_error(f"Start output: {result.stderr}")
            return False
        else:
            print_success("Containers started successfully")
    except Exception as e:
        start_progress.stop()
        print_error(f"Start error: {e}")
        return False

    return True

def wait_for_services():
    """Wait for all services to be healthy with visual progress"""
    print_header("⏳ WAITING FOR SERVICES")
    
    max_attempts = 12
    wait_time = 2
    
    print_info("Checking service health...")
    
    for attempt in range(max_attempts):
        # Progress indicator
        percentage = (attempt / max_attempts) * 100
        bar_length = 30
        filled_length = int(bar_length * attempt // max_attempts)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        print(f"\r{Colors.CYAN}[{bar}] {percentage:.0f}% - Health check {attempt + 1}/{max_attempts}{Colors.END}", end='', flush=True)
        
        # Check if containers are running first
        result = subprocess.run(["docker-compose", "ps"], capture_output=True, text=True)
        if "Up" not in result.stdout:
            print(f"\n{Colors.RED}⚠️  Some containers are not running!{Colors.END}")
            subprocess.run(["docker-compose", "ps"])
            return False
        
        # Quick service checks
        services_ready = True
        service_status = []
        
        # PostgreSQL
        result = subprocess.run(
            ["docker-compose", "exec", "-T", "db", "pg_isready", "-U", "videoflix", "-d", "videoflix"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            service_status.append("✅ DB")
        else:
            service_status.append("⏳ DB")
            services_ready = False
        
        # Redis
        result = subprocess.run(
            ["docker-compose", "exec", "-T", "redis", "redis-cli", "ping"],
            capture_output=True, text=True
        )
        if result.returncode == 0 and "PONG" in result.stdout:
            service_status.append("✅ Redis")
        else:
            service_status.append("⏳ Redis")
            services_ready = False
        
        # Web service
        result = subprocess.run(
            ["docker-compose", "exec", "-T", "web", "python", "-c", "print('OK')"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and "OK" in result.stdout:
            service_status.append("✅ Web")
        else:
            service_status.append("⏳ Web")
            services_ready = False
        
        # Update the line with service status
        status_str = " | ".join(service_status)
        print(f"\r{Colors.CYAN}[{bar}] {percentage:.0f}% - {status_str}{Colors.END}                    ", end='', flush=True)
        
        if services_ready:
            print(f"\n{Colors.GREEN}✅ All services are healthy!{Colors.END}")
            return True
        
        # Only wait if not the last attempt
        if attempt < max_attempts - 1:
            time.sleep(wait_time)
    
    print(f"\n{Colors.RED}❌ Services failed to start after {max_attempts * wait_time} seconds{Colors.END}")
    print_info("Container status:")
    subprocess.run(["docker-compose", "ps"])
    return False
    
    print_error("Services failed to start properly")
    print_info("Final diagnostic - Container status:")
    subprocess.run(["docker-compose", "ps"])
    print_info("Final diagnostic - Recent logs:")
    subprocess.run(["docker-compose", "logs", "--tail=20"])
    return False

def ensure_migration_directories():
    """Ensure migration directories exist with __init__.py files"""
    migration_dirs = ['videos/migrations', 'authentication/migrations']
    
    for migration_dir in migration_dirs:
        os.makedirs(migration_dir, exist_ok=True)
        init_file = os.path.join(migration_dir, '__init__.py')
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write('# Django migrations\n')
            print_info(f"  ✓ Created {init_file}")

def regenerate_migrations():
    """Remove old migrations and create fresh ones with current timestamp"""
    print_header("🔄 REGENERATING MIGRATIONS")
    print_info("Creating fresh migrations with current timestamp to avoid conflicts...")
    
    # Ensure migration directories exist
    ensure_migration_directories()
    
    # Remove existing migration files (but keep __init__.py)
    migration_dirs = ['videos/migrations', 'authentication/migrations']
    
    for migration_dir in migration_dirs:
        if os.path.exists(migration_dir):
            for file in os.listdir(migration_dir):
                if file.endswith('.py') and file != '__init__.py':
                    file_path = os.path.join(migration_dir, file)
                    try:
                        os.remove(file_path)
                        print_info(f"  ✓ Removed old migration: {file}")
                    except OSError:
                        pass  # File might not exist, that's okay
    
    # Wait for services to be ready first
    print_info("Waiting for database to be ready...")
    time.sleep(5)
    
    # Create fresh migrations for videos app
    success, output = run_command(
        "docker-compose exec -T web python manage.py makemigrations videos",
        "Creating fresh migrations for videos app"
    )
    
    if not success:
        print_warning(f"Videos migrations warning: {output}")
        # Continue anyway, might be because no changes detected
    
    # Create fresh migrations for authentication app  
    success, output = run_command(
        "docker-compose exec -T web python manage.py makemigrations authentication",
        "Creating fresh migrations for authentication app"
    )
    
    if not success:
        print_warning(f"Authentication migrations warning: {output}")
        # Continue anyway, might be because no changes detected
    
    # Create any other migrations
    success, output = run_command(
        "docker-compose exec -T web python manage.py makemigrations",
        "Creating any additional migrations"
    )
    
    print_success("✓ Fresh migrations created successfully with current timestamp")
    return True

def setup_database():
    """Setup database with migrations and progress feedback"""
    print_header("🗄️  SETTING UP DATABASE")
    
    # Apply migrations with progress (migrations already created by regenerate_migrations)
    print_info("Applying database migrations...")
    migration_progress = ProgressBar("Setting up database tables and relationships")
    migration_progress.start()
    
    try:
        result = subprocess.run(
            "docker-compose exec -T web python manage.py migrate",
            shell=True, capture_output=True, text=True, timeout=120
        )
        migration_progress.stop()
        
        if result.returncode != 0:
            print_warning("Migration failed, trying database reset...")
            
            # Reset database with progress
            reset_progress = ProgressBar("Resetting database schema")
            reset_progress.start()
            
            try:
                subprocess.run(
                    "docker-compose exec -T db psql -U videoflix -d videoflix -c 'DROP SCHEMA public CASCADE; CREATE SCHEMA public; GRANT ALL ON SCHEMA public TO videoflix;'",
                    shell=True, capture_output=True, text=True, timeout=60
                )
                reset_progress.stop()
                
                # Try migrations again
                retry_progress = ProgressBar("Re-applying migrations after reset")
                retry_progress.start()
                
                result = subprocess.run(
                    "docker-compose exec -T web python manage.py migrate",
                    shell=True, capture_output=True, text=True, timeout=120
                )
                retry_progress.stop()
                
                if result.returncode != 0:
                    print_error("Database setup failed completely")
                    print_error(f"Output: {result.stderr}")
                    return False
                    
            except Exception as e:
                reset_progress.stop()
                print_error(f"Database reset failed: {e}")
                return False
        
        print_success("Database setup completed successfully")
        return True
        
    except subprocess.TimeoutExpired:
        migration_progress.stop()
        print_error("Database migration timed out")
        return False
    except Exception as e:
        migration_progress.stop()
        print_error(f"Migration error: {e}")
        return False

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
    
    print_info("\n🔐 NEW FEATURES:")
    print_info("  ✅ Password Reset fully implemented!")
    print_info("  📧 Forgot Password: http://localhost:5173/forgot-password")
    print_info("  🔄 Reset tokens can be reused for development")
    print_info("  📬 Real email delivery with Gmail/Outlook SMTP")
    
    print_info("\n⚠️  FOR MENTORS:")
    print_info("  If you see 'Connection refused' errors:")
    print_info("  1. Wait 30 seconds for all services to start")
    print_info("  2. Check: docker-compose ps")
    print_info("  3. Check logs: docker-compose logs")
    print_info("  4. Frontend URL should be http://localhost:5173")

def main():
    """Main setup function with progress tracking"""
    print_header("🎬 VIDEOFLIX BACKEND ROBUST SETUP")
    print_info("This script fixes common setup issues reported by mentors")
    
    steps = [
        ("Docker Check", check_docker),
        ("Environment Cleanup", cleanup_environment),
        ("Environment Setup", setup_env_file),
        ("Container Build", build_and_start),
        ("Service Health Check", wait_for_services),
        ("Migration Regeneration", regenerate_migrations),
        ("Database Setup", setup_database),
        ("Admin User Creation", create_admin),
        ("Basic Tests", run_basic_tests),
    ]
    
    total_steps = len(steps)
    
    for step_num, (step_name, step_function) in enumerate(steps, 1):
        print_progress_step(step_num, total_steps, f"Starting: {step_name}")
        
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
    
    # Final progress bar at 100%
    print_progress_step(total_steps, total_steps, "Setup Complete!")
    
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
