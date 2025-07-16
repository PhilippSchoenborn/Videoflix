@echo off
echo.
echo ========================================
echo  VIDEOFLIX BACKEND - SCHNELLSTART
echo ========================================
echo.

echo Pruefe Docker Desktop...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo FEHLER: Docker Desktop ist nicht installiert oder nicht gestartet!
    echo Bitte starten Sie Docker Desktop und versuchen Sie es erneut.
    pause
    exit /b 1
)

echo Docker Desktop ist bereit!
echo.

echo Starte Docker Container...
docker-compose up -d --build

echo.
echo Warte auf Container-Start...
timeout /t 10 >nul

echo.
echo Richte Datenbank ein...
docker-compose exec -T web python manage.py migrate

echo.
echo Erstelle Admin-User...
docker-compose exec -T web python create_admin.py

echo.
echo Verifiziere Admin-User...
docker-compose exec -T web python verify_admin.py

echo.
echo ========================================
echo  VIDEOFLIX BACKEND IST BEREIT!
echo ========================================
echo.
echo  Backend URL: http://localhost:8000
echo  Admin Panel: http://localhost:8000/admin
echo.
echo  Admin-Anmeldedaten:
echo  E-Mail: admin@test.com
echo  Passwort: admin123456
echo.
echo  Druecken Sie eine Taste zum Beenden...
pause >nul
