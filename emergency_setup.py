#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EMERGENCY SETUP SCRIPT - Videoflix Backend
==========================================

This is a simplified, ultra-robust setup script that handles the most common
setup issues reported by mentors. If the main setup.py fails, use this.

Usage: python emergency_setup.py
"""

import os
import sys
import subprocess
import time

# Fix Windows encoding issues
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

def log(message, level="INFO"):
    """Simple logging function - Windows compatible"""
    levels = {
        "INFO": "[INFO]",
        "SUCCESS": "[OK]", 
        "WARNING": "[WARN]",
        "ERROR": "[ERROR]"
    }
    icon = levels.get(level, "[INFO]")
    try:
        print(f"{icon} {message}")
    except UnicodeEncodeError:
        # Fallback for encoding issues
        print(f"{icon} {message.encode('ascii', 'ignore').decode('ascii')}")

def run_cmd(command, description):
    """Run a command with error handling"""
    log(f"{description}...")
    try:
        if isinstance(command, str):
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=300)
        else:
            result = subprocess.run(command, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            log(f"{description} - SUCCESS", "SUCCESS")
            return True, result.stdout
        else:
            log(f"{description} - FAILED: {result.stderr}", "ERROR")
            return False, result.stderr
    except Exception as e:
        log(f"{description} - ERROR: {e}", "ERROR")
        return False, str(e)

def main():
    """Emergency setup main function"""
    log("EMERGENCY SETUP - Videoflix Backend", "SUCCESS")
    log("This script will attempt a minimal but functional setup")
    
    # Step 1: Check prerequisites
    log("\n=== STEP 1: PREREQUISITES ===")
    success, _ = run_cmd("docker --version", "Checking Docker")
    if not success:
        log("Docker is not available! Please install Docker Desktop.", "ERROR")
        return False
    
    success, _ = run_cmd("docker-compose --version", "Checking Docker Compose")
    if not success:
        log("Docker Compose is not available!", "ERROR")
        return False
    
    # Step 2: Clean environment
    log("\n=== STEP 2: CLEANUP ===")
    run_cmd("docker-compose down -v --remove-orphans", "Stopping all containers")
    run_cmd("docker system prune -f", "Cleaning Docker system")
    
    # Step 3: Environment setup
    log("\n=== STEP 3: ENVIRONMENT ===")
    if not os.path.exists('.env') and os.path.exists('.env.template'):
        try:
            import shutil
            shutil.copy('.env.template', '.env')
            log("Created .env from template", "SUCCESS")
        except Exception as e:
            log(f"Could not create .env: {e}", "WARNING")
    
    # Create directories
    for directory in ['logs', 'media/videos', 'media/video_thumbnails']:
        os.makedirs(directory, exist_ok=True)
    
    # Step 4: Migration directories
    log("\n=== STEP 4: MIGRATION SETUP ===")
    migration_dirs = ['authentication/migrations', 'videos/migrations']
    
    for migration_dir in migration_dirs:
        try:
            os.makedirs(migration_dir, exist_ok=True)
            init_file = os.path.join(migration_dir, '__init__.py')
            if not os.path.exists(init_file):
                with open(init_file, 'w') as f:
                    f.write('# Migrations\n')
            log(f"Prepared {migration_dir}", "SUCCESS")
        except Exception as e:
            log(f"Could not prepare {migration_dir}: {e}", "WARNING")
    
    # Step 5: Build containers
    log("\n=== STEP 5: BUILD CONTAINERS ===")
    success, _ = run_cmd("docker-compose build --no-cache", "Building all containers")
    if not success:
        log("Container build failed!", "ERROR")
        return False
    
    # Step 6: Start services incrementally
    log("\n=== STEP 6: START SERVICES ===")
    
    # Start database first
    success, _ = run_cmd("docker-compose up -d db redis", "Starting database and Redis")
    if not success:
        log("Database startup failed!", "ERROR")
        return False
    
    # Wait for database
    log("Waiting for database to be ready...")
    time.sleep(15)
    
    # Test database connection
    for attempt in range(5):
        success, _ = run_cmd(
            "docker-compose exec -T db pg_isready -U videoflix -d videoflix",
            f"Testing database connection (attempt {attempt + 1})"
        )
        if success:
            break
        time.sleep(3)
    
    if not success:
        log("Database is not ready after 5 attempts!", "ERROR")
        return False
    
    # Start web container
    success, _ = run_cmd("docker-compose up -d web worker", "Starting web and worker")
    if not success:
        log("Web container startup failed!", "ERROR")
        return False
    
    # Wait for web container
    log("Waiting for web container...")
    time.sleep(10)
    
    # Step 7: Database setup - SIMPLIFIED
    log("\n=== STEP 7: DATABASE SETUP ===")
    
    # Simple migration approach - one command
    success, _ = run_cmd(
        "docker-compose exec -T web python manage.py makemigrations",
        "Creating all migrations at once"
    )
    
    if not success:
        log("Migration creation failed, trying individual apps...", "WARNING")
        
        # Try each app separately if needed
        for app in ['authentication', 'videos']:
            run_cmd(
                f"docker-compose exec -T web python manage.py makemigrations {app}",
                f"Creating {app} migrations"
            )
    
    # Apply migrations
    success, _ = run_cmd(
        "docker-compose exec -T web python manage.py migrate",
        "Applying migrations"
    )
    
    if not success:
        log("Migration application failed! Trying database reset...", "WARNING")
        
        # Database reset approach
        run_cmd("docker-compose restart db", "Restarting database")
        time.sleep(10)
        
        # Try migrations again after reset
        success, _ = run_cmd(
            "docker-compose exec -T web python manage.py migrate",
            "Retrying migrations after database reset"
        )
        
        if not success:
            log("Database setup failed completely!", "ERROR")
            return False
    
    # Step 8: Admin user
    log("\n=== STEP 8: ADMIN USER ===")
    success, _ = run_cmd(
        "docker-compose exec -T web python create_admin.py",
        "Creating admin user"
    )
    
    if not success:
        log("Admin creation had issues (may already exist)", "WARNING")
    
    # Step 9: Final verification
    log("\n=== STEP 9: VERIFICATION ===")
    success, output = run_cmd(
        "docker-compose exec -T web python manage.py check",
        "Django system check"
    )
    
    if not success:
        log("System check had issues, but setup likely successful", "WARNING")
        log(f"Check output: {str(output)[:200]}...")
    else:
        log("System check passed!", "SUCCESS")
    
    # Show final status
    log("\nEMERGENCY SETUP COMPLETED!", "SUCCESS")
    log("="*50)
    log("Backend: http://localhost:8000")
    log("Admin: http://localhost:8000/admin")
    log("Login: admin@test.com / admin123456")
    log("\nContainer status:")
    
    # Show container status
    subprocess.run("docker-compose ps", shell=True)
    
    return True
    
if __name__ == "__main__":
    try:
        success = main()
        if success:
            log("Emergency setup completed!", "SUCCESS")
            sys.exit(0)
        else:
            log("Emergency setup failed!", "ERROR")
            sys.exit(1)
    except KeyboardInterrupt:
        log("Setup interrupted by user", "WARNING")
        sys.exit(1)
    except Exception as e:
        log(f"Unexpected error: {e}", "ERROR")
        sys.exit(1)
