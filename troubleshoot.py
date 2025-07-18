#!/usr/bin/env python3
"""
🛠️ Videoflix Troubleshooting Script
===================================

This script diagnoses and fixes common Docker setup issues.
Run this if the main setup.py fails.
"""

import subprocess
import time

def check_docker_status():
    """Check detailed Docker status"""
    print("🔍 DOCKER DIAGNOSIS")
    print("=" * 50)
    
    # Check Docker daemon
    try:
        result = subprocess.run(["docker", "info"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Docker daemon is running")
        else:
            print("❌ Docker daemon not responding")
            return False
    except:
        print("❌ Docker not found or not running")
        return False
    
    # Check available resources
    try:
        result = subprocess.run(["docker", "system", "df"], capture_output=True, text=True)
        print(f"💾 Docker system usage:\n{result.stdout}")
    except:
        pass
    
    return True

def force_cleanup():
    """Force clean all Docker resources"""
    print("\n🧹 FORCE CLEANUP")
    print("=" * 50)
    
    commands = [
        "docker-compose down -v --remove-orphans",
        "docker container prune -f",
        "docker volume prune -f", 
        "docker network prune -f",
        "docker image prune -f",
        "docker system prune -a -f"
    ]
    
    for cmd in commands:
        print(f"Running: {cmd}")
        try:
            subprocess.run(cmd, shell=True, capture_output=True)
            print("✅ Success")
        except:
            print("⚠️ Warning")
        time.sleep(2)

def check_ports():
    """Check if required ports are available"""
    print("\n🔌 PORT CHECK")
    print("=" * 50)
    
    ports = [5432, 6379, 8000]
    for port in ports:
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            
            if result == 0:
                print(f"⚠️ Port {port} is already in use")
            else:
                print(f"✅ Port {port} is available")
        except:
            print(f"❓ Could not check port {port}")

def minimal_setup():
    """Try minimal container setup"""
    print("\n🚀 MINIMAL SETUP ATTEMPT")
    print("=" * 50)
    
    # Just try to start database first
    print("Starting database only...")
    result = subprocess.run("docker-compose up -d db", shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Database container started")
        
        # Wait and test
        print("Waiting for database...")
        time.sleep(15)
        
        db_test = subprocess.run(
            ["docker-compose", "exec", "-T", "db", "pg_isready", "-U", "postgres"],
            capture_output=True, text=True
        )
        
        if db_test.returncode == 0:
            print("✅ Database is responding")
            
            # Try Redis
            print("Starting Redis...")
            subprocess.run("docker-compose up -d redis", shell=True, capture_output=True)
            time.sleep(5)
            
            redis_test = subprocess.run(
                ["docker-compose", "exec", "-T", "redis", "redis-cli", "ping"],
                capture_output=True, text=True
            )
            
            if redis_test.returncode == 0:
                print("✅ Redis is responding")
                
                # Try web service
                print("Starting web service...")
                subprocess.run("docker-compose up -d web", shell=True, capture_output=True)
                
                return True
        else:
            print("❌ Database not responding")
    else:
        print("❌ Failed to start database")
        print(f"Error: {result.stderr}")
    
    return False

def main():
    print("🛠️ VIDEOFLIX TROUBLESHOOTING")
    print("=" * 60)
    print("This script helps diagnose Docker setup issues")
    print()
    
    # Step 1: Check Docker
    if not check_docker_status():
        print("\n❌ Docker issues detected!")
        print("Please ensure Docker Desktop is running and try again.")
        return
    
    # Step 2: Check ports
    check_ports()
    
    # Step 3: Force cleanup
    print("\nCleaning up old containers...")
    force_cleanup()
    
    # Step 4: Try minimal setup
    print("\nAttempting minimal setup...")
    if minimal_setup():
        print("\n✅ Minimal setup successful!")
        print("Now try running the main setup.py script")
    else:
        print("\n❌ Minimal setup failed")
        print("Please check Docker Desktop settings:")
        print("- Ensure enough memory allocated (4GB+)")
        print("- Check if virtualization is enabled")
        print("- Try restarting Docker Desktop")

if __name__ == "__main__":
    main()
