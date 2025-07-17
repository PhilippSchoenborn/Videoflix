# E-Mail Testing für Videoflix

## 📧 E-Mail-Konfiguration

Das System ist für Development-Testing konfiguriert. E-Mails werden **nicht** live verschickt, sondern werden für Testing-Zwecke in Dateien gespeichert.

## 📁 Wo finde ich E-Mails?

E-Mails werden in folgenden Ordner gespeichert:
```
logs/emails/
```

## 🔍 E-Mail-Funktionen testen

### 1. **Registrierung**
- Registriere einen neuen User über das Frontend
- E-Mail-Verifizierung wird in `logs/emails/` gespeichert
- Öffne die Datei und kopiere den Verifizierungslink

### 2. **Passwort-Reset**
- Verwende "Passwort vergessen" im Frontend
- E-Mail wird in `logs/emails/` gespeichert
- Öffne die Datei und kopiere den Reset-Link

### 3. **E-Mail-Dateien überprüfen**
```bash
# Container-Logs für E-Mail-Debugging
docker-compose logs web | grep -i email

# Zugriff auf E-Mail-Dateien
docker-compose exec web ls -la logs/emails/
docker-compose exec web cat logs/emails/[DATEINAME]
```

## ⚙️ Konfiguration für Live-E-Mails

Für Live-E-Mails (Production), ändere in `.env`:
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
```

## 🐛 Troubleshooting

### E-Mail-Dateien werden nicht erstellt?
1. Überprüfe ob `logs/emails/` Ordner existiert
2. Überprüfe Container-Logs: `docker-compose logs web`
3. Teste manuell: `docker-compose exec web python manage.py shell`

### E-Mail-Links funktionieren nicht?
- Überprüfe `FRONTEND_URL` in `.env`
- Standard: `http://localhost:5173`

## 📋 Test-Checkliste

- [ ] User-Registrierung → E-Mail in logs/emails/
- [ ] E-Mail-Verifizierung → Link funktioniert
- [ ] Passwort-Reset → E-Mail in logs/emails/
- [ ] Reset-Link → Funktioniert korrekt
