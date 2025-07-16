#!/usr/bin/env python3
"""
🔄 Videoflix Backend - Reset Script
==================================

This script resets the entire backend and fixes common issues.
"""

import subprocess
import time
import os

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
    """Executes a command and returns the status"""
    print_info(f"Executing: {description}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print_success(f"{description} - Successful")
            return True
        else:
            print_error(f"{description} - Failed: {result.stderr}")
            return False
    except Exception as e:
        print_error(f"{description} - Error: {str(e)}")
        return False

def reset_system():
    """Resets the entire system"""
    print_header("🔄 SYSTEM RESET")
    
    # 1. Stop containers
    run_command("docker-compose down", "Stop containers")
    
    # 2. Delete volumes
    print_warning("Deleting all database volumes (all data will be lost!)")
    run_command("docker-compose down -v", "Delete volumes")
    
    # 3. Clean Docker system
    run_command("docker system prune -f", "Clean Docker system")
    
    # 4. Rebuild containers
    run_command("docker-compose up -d --build", "Rebuild containers")
    
    # 5. Wait
    print_info("Waiting for containers to start...")
    time.sleep(20)
    
    # 6. Run migrations
    run_command("docker-compose exec -T web python manage.py migrate", "Migrate database")
    
    # 7. Create admin user
    run_command("docker-compose exec -T web python create_admin.py", "Create admin user")
    
    # 8. Verify admin user
    run_command("docker-compose exec -T web python verify_admin.py", "Verify admin user")
    
    print_header("✅ SYSTEM RESET COMPLETED")
    print_success("System was successfully reset!")
    print("")
    print("📋 Access credentials:")
    print("  • Backend: http://localhost:8000")
    print("  • Admin: http://localhost:8000/admin")
    print("  • Login: admin@test.com / admin123456")

def main():
    """Main function"""
    print_header("🔄 VIDEOFLIX BACKEND RESET")
    print("This script resets the entire backend.")
    print_warning("WARNING: All data in the database will be lost!")
    
    # Confirmation
    response = input(f"\n{Colors.YELLOW}Do you want to reset the system? (y/n): {Colors.END}")
    if response.lower() not in ['y', 'yes', 'j', 'ja']:
        print("Reset cancelled.")
        return
    
    reset_system()

if __name__ == "__main__":
    main()
