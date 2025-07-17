# Video-Upload Fix für Videoflix

## 🎬 Video-Upload-Problem behoben

**Problem:** Videos mussten zweimal hochgeladen werden, da der Worker nicht lief.

**Lösung:** RQ-Worker-Service zu Docker-Compose hinzugefügt.

## 🔧 Was wurde geändert?

1. **RQ-Worker-Service** in `docker-compose.yml` hinzugefügt
2. **E-Mail-Backend** auf File-basiert geändert für bessere Testbarkeit
3. **Dokumentation** für E-Mail-Testing hinzugefügt

## 🚀 Wie funktioniert Video-Upload jetzt?

### 1. Video-Upload-Prozess:
```
1. User lädt Video hoch → Video wird in DB gespeichert
2. Signal triggert → RQ-Worker startet Verarbeitung
3. Worker generiert → Verschiedene Qualitäten (120p, 360p, 720p, 1080p)
4. Worker erstellt → Thumbnail aus Video
5. Worker berechnet → Video-Dauer
6. Status wird → Auf "processed" gesetzt
```

### 2. Neuer Worker-Service:
```yaml
worker:
  build:
    context: .
    dockerfile: backend.Dockerfile
  command: python manage.py rqworker default
  volumes:
    - .:/app
  depends_on:
    db:
      condition: service_healthy
    redis:
      condition: service_healthy
  env_file:
    - .env
  networks:
    - videoflix_network
  restart: unless-stopped
```

## 🔍 Video-Upload debugging

### Container-Status überprüfen:
```bash
docker-compose ps
```

### Worker-Logs überprüfen:
```bash
docker-compose logs worker
```

### Redis-Queue Status:
```bash
docker-compose exec web python manage.py rqstats
```

### Video-Verarbeitung manuell testen:
```bash
docker-compose exec web python manage.py shell
from videos.utils import process_video_upload
process_video_upload(VIDEO_ID)
```

## ✅ Test-Checkliste

- [ ] Video-Upload → Erfolg beim ersten Mal
- [ ] Worker-Logs → Verarbeitung startet automatisch
- [ ] Video-Qualitäten → Werden generiert (120p, 360p, 720p, 1080p)
- [ ] Thumbnail → Wird erstellt
- [ ] Video-Dauer → Wird berechnet
- [ ] Status → Wird auf "processed" gesetzt

## 🐛 Troubleshooting

### Video wird nicht verarbeitet?
1. Worker-Service läuft: `docker-compose ps`
2. Redis-Verbindung: `docker-compose logs redis`
3. Worker-Logs: `docker-compose logs worker`

### Verarbeitung hängt?
1. FFmpeg installiert: `docker-compose exec web ffmpeg -version`
2. Speicherplatz: `docker-compose exec web df -h`
3. Worker-Timeout: Standard 30 Minuten

### Qualitäten fehlen?
1. Überprüfe Video-Format (MP4 empfohlen)
2. Überprüfe Video-Größe (< 2GB empfohlen)
3. Überprüfe FFmpeg-Logs in Worker
