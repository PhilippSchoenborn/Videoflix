#!/usr/bin/env python3
"""
🔍 Videoflix Backend - Validation Script
=========================================

Checks if the backend is correctly installed and functional.
"""

import requests
import subprocess
import json
import time
import os
from pathlib import Path

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

def check_docker_containers():
    """Checks if all Docker containers are running"""
    print_header("🐳 CHECKING DOCKER CONTAINERS")
    
    try:
        result = subprocess.run(
            ["docker-compose", "ps", "--format", "json"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print_error("Docker-compose is not available")
            return False
        
        containers = []
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                containers.append(json.loads(line))
        
        required_services = ['web', 'db', 'redis']
        running_services = []
        
        for container in containers:
            service = container.get('Service', '')
            state = container.get('State', '')
            
            if service in required_services:
                if state == 'running':
                    print_success(f"Service '{service}' is running")
                    running_services.append(service)
                else:
                    print_error(f"Service '{service}' is not active (Status: {state})")
        
        missing_services = set(required_services) - set(running_services)
        if missing_services:
            print_error(f"Missing services: {', '.join(missing_services)}")
            return False
        
        print_success("All Docker containers are running correctly")
        return True
        
    except Exception as e:
        print_error(f"Error checking containers: {str(e)}")
        return False

def check_backend_api():
    """Checks if the backend API is reachable"""
    print_header("🌐 CHECKING BACKEND API")
    
    base_url = "http://localhost:8000"
    
    # Health check
    try:
        response = requests.get(f"{base_url}/admin/", timeout=10)
        if response.status_code == 200:
            print_success("Backend is reachable")
        else:
            print_error(f"Backend responds with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"Backend is not reachable: {str(e)}")
        return False
    
    # Check API endpoints
    endpoints = [
        "/api/",
        "/api/register/",
        "/api/login/",
        "/api/videos/",
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code in [200, 405, 401]:  # 405 = Method not allowed is OK
                print_success(f"Endpoint {endpoint} is available")
            else:
                print_warning(f"Endpoint {endpoint} responds with status {response.status_code}")
        except requests.exceptions.RequestException as e:
            print_error(f"Endpoint {endpoint} is not reachable: {str(e)}")
    
    return True

def check_admin_login():
    """Checks if admin login works"""
    print_header("🔑 CHECKING ADMIN LOGIN")
    
    try:
        session = requests.Session()
        
        # Get CSRF token
        response = session.get("http://localhost:8000/admin/login/", timeout=10)
        if response.status_code != 200:
            print_error("Admin login page not reachable")
            return False
        
        # Extract CSRF token
        csrf_token = None
        for line in response.text.split('\n'):
            if 'csrfmiddlewaretoken' in line and 'value=' in line:
                csrf_token = line.split('value="')[1].split('"')[0]
                break
        
        if not csrf_token:
            print_error("CSRF token not found")
            return False
        
        # Login attempt
        login_data = {
            'username': 'admin@test.com',
            'password': 'admin123456',
            'csrfmiddlewaretoken': csrf_token,
            'next': '/admin/'
        }
        
        response = session.post(
            "http://localhost:8000/admin/login/",
            data=login_data,
            timeout=10
        )
        
        if response.status_code == 200 and '/admin/' in response.url:
            print_success("Admin login works")
            return True
        else:
            print_error("Admin login failed")
            return False
            
    except Exception as e:
        print_error(f"Error during admin login: {str(e)}")
        return False

def check_database():
    """Checks database connection"""
    print_header("🗄️  CHECKING DATABASE")
    
    try:
        result = subprocess.run(
            ["docker-compose", "exec", "-T", "web", "python", "manage.py", "check", "--database", "default"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print_success("Database connection works")
            return True
        else:
            print_error(f"Database problem: {result.stderr}")
            return False
            
    except Exception as e:
        print_error(f"Error during database check: {str(e)}")
        return False

def check_files():
    """Checks important files"""
    print_header("📁 CHECKING FILES")
    
    required_files = [
        '.env',
        'docker-compose.yml',
        'requirements.txt',
        'manage.py',
        'create_admin.py',
        'verify_admin.py',
    ]
    
    all_files_exist = True
    
    for file in required_files:
        if os.path.exists(file):
            print_success(f"File {file} exists")
        else:
            print_error(f"File {file} missing")
            all_files_exist = False
    
    # Check directories
    required_dirs = [
        'logs',
        'media',
        'authentication',
        'videos',
        'core',
    ]
    
    for dir in required_dirs:
        if os.path.exists(dir):
            print_success(f"Directory {dir} exists")
        else:
            print_error(f"Directory {dir} missing")
            all_files_exist = False
    
    return all_files_exist

def run_basic_tests():
    """Runs basic tests"""
    print_header("🧪 BASIC TESTS")
    
    try:
        result = subprocess.run(
            ["docker-compose", "exec", "-T", "web", "python", "manage.py", "test", "authentication.tests", "--verbosity=0"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print_success("Basic tests successful")
            return True
        else:
            print_warning(f"Some tests failed: {result.stderr}")
            return False
            
    except Exception as e:
        print_error(f"Error running tests: {str(e)}")
        return False

def print_summary(results):
    """Prints a summary"""
    print_header("📊 VALIDATION SUMMARY")
    
    total_checks = len(results)
    passed_checks = sum(1 for result in results.values() if result)
    
    print(f"Total checks: {total_checks}")
    print(f"Successful: {passed_checks}")
    print(f"Failed: {total_checks - passed_checks}")
    
    if passed_checks == total_checks:
        print_success("\n🎉 ALL CHECKS SUCCESSFUL!")
        print_success("The backend is fully functional!")
    else:
        print_error(f"\n❌ {total_checks - passed_checks} CHECKS FAILED!")
        print_warning("Please fix the issues and run the validation again.")
    
    print("\n" + "="*60)
    print("DETAILED RESULTS:")
    print("="*60)
    
    for check, result in results.items():
        status = "✅ SUCCESSFUL" if result else "❌ FAILED"
        print(f"{check}: {status}")

def main():
    """Main function"""
    print_header("🔍 VIDEOFLIX BACKEND VALIDATION")
    print("Checks the complete functionality of the backend.")
    
    # Wait for container startup
    print_info("Waiting for containers to start...")
    time.sleep(3)
    
    # Run all checks
    results = {}
    
    results["Docker Containers"] = check_docker_containers()
    results["Important Files"] = check_files()
    results["Database Connection"] = check_database()
    results["Backend API"] = check_backend_api()
    results["Admin Login"] = check_admin_login()
    results["Basic Tests"] = run_basic_tests()
    
    # Summary
    print_summary(results)

if __name__ == "__main__":
    main()
