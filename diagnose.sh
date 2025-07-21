#!/bin/bash
# diagnose.sh - Vollständige Systemdiagnose

echo "🔍 VIDEOFLIX BACKEND DIAGNOSIS"
echo "================================"

echo "📋 System Information:"
echo "OS: $(uname -a)"
echo "Docker: $(docker --version)"
echo "Docker Compose: $(docker-compose --version)"

echo ""
echo "🐳 Container Status:"
docker-compose ps

echo ""
echo "📊 Container Logs (last 50 lines):"
echo "--- WEB CONTAINER ---"
docker-compose logs --tail=50 web

echo ""
echo "--- DB CONTAINER ---"  
docker-compose logs --tail=50 db

echo ""
echo "🔍 Environment Variables:"
docker-compose exec web env | grep -E "(DB_|POSTGRES_|DJANGO_)"

echo ""
echo "🗃️ Database Connection Test:"
docker-compose exec web python manage.py check --database default

echo ""
echo "📋 Migration Status:"
docker-compose exec web python manage.py showmigrations

echo ""
echo "🔗 Network Connectivity:"
docker-compose exec web ping -c 3 db

echo ""  
echo "💾 Database Content:"
docker-compose exec db psql -U videoflix -d videoflix -c "\dt"

echo ""
echo "🔍 Diagnosis Complete!"
