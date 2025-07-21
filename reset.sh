#!/bin/bash
# reset.sh - Kompletter Reset

echo "🚨 COMPLETE VIDEOFLIX RESET"
echo "==========================="

echo "⏹️ Stopping all containers..."
docker-compose down

echo "🗑️ Removing volumes..."
docker volume rm videoflix-main_postgres_data || true
docker volume rm videoflix-main_redis_data || true

echo "🧹 Cleaning Docker system..."
docker system prune -f

echo "🔄 Removing migration files..."
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

echo "📁 Recreating .env from template..."
cp .env.template .env

echo "🚀 Starting fresh build..."
docker-compose up -d --build

echo "✅ Reset complete! Check with: docker-compose ps"
