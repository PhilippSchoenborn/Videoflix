# 🎯 QUICK-TEST CHECKLIST

## ✅ 5-MINUTEN-TEST für Mentoren

### 1. Installation (30 Sekunden)
```bash
python setup.py
```
**Erwartung:** Grüne Häkchen, keine roten Fehler

### 2. Backend-Zugang (30 Sekunden)
- Browser: http://localhost:8000/admin
- Login: admin@test.com / admin123456
**Erwartung:** Admin-Panel lädt, Login funktioniert

### 3. API-Test (60 Sekunden)
```bash
# Terminal/PowerShell:
curl http://localhost:8000/api/
curl http://localhost:8000/api/videos/
curl http://localhost:8000/api/register/
```
**Erwartung:** JSON-Responses, keine 500-Fehler

### 4. System-Validierung (60 Sekunden)
```bash
python validate.py
```
**Erwartung:** Alle Prüfungen ✅ ERFOLGREICH

### 5. Tests (120 Sekunden)
```bash
docker-compose exec web python manage.py test authentication
```
**Erwartung:** Tests laufen durch, keine Failures

## 🎖️ BEWERTUNG

- **Alle 5 Tests bestanden:** A+ (Excellent)
- **4 Tests bestanden:** A (Very Good)
- **3 Tests bestanden:** B (Good)
- **2 Tests bestanden:** C (Satisfactory)
- **1 Test bestanden:** D (Needs Improvement)
- **0 Tests bestanden:** F (Fail)

## 📝 NOTIZEN
_Platz für Mentor-Kommentare:_

_______________________________________________
_______________________________________________
_______________________________________________
