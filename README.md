# 🎬 Videoflix - Backend API

## 🚀 Installation & Quickstart

### Voraussetzungen
- Docker Desktop (inkl. docker-compose)
- Git
- 8GB+ RAM empfohlen

### Setup & Start
1. **Repository klonen**
   ```bash
   git clone <repository-url>
   cd videoflix-backend
   ```
2. **Umgebungsvariablen anlegen**
   ```bash
   cp .env.template .env
   # Passe .env nach Bedarf an
   ```
3. **Docker-Container starten**
   ```bash
   docker-compose up --build
   # oder
   docker compose up --build
   ```
4. **Migrationen & Superuser**
   ```bash
   docker exec videoflix-web python manage.py migrate
   docker exec -it videoflix-web python manage.py createsuperuser
   ```
5. **Zugriff**
   - API: http://localhost:8000
   - Admin: http://localhost:8000/admin
   - API Docs: http://localhost:8000/api/

---

## 🧑‍💻 Implementierung & Entwicklung

- **Backend:** Django 5 + Django REST Framework
- **Datenbank:** PostgreSQL (Docker)
- **Cache/Queue:** Redis, Django RQ
- **Testing:** pytest (+ coverage)
- **Container:** Docker Compose

### Projektstruktur (Kurz)
- `authentication/` – User/Auth-API
- `videos/` – Video-API & Streaming
- `core/` – Django Settings
- `tests/` – Testfälle

---

## 🧪 Testing & Coverage

**Tests im Container ausführen:**
```bash
docker exec videoflix-web pytest
# Mit Coverage:
docker exec videoflix-web pytest --cov=.
```
**Testdateien müssen mit `test_` beginnen!**

**Coverage-Report (HTML):**
```bash
docker exec videoflix-web pytest --cov=. --cov-report=html
```

---

## ✅ Definition of Done (DoD) – Checkliste
- [x] Docker-Setup & Start funktioniert
- [x] API-URLs an Frontend angepasst
- [x] Auth & Streaming funktionieren fehlerfrei
- [x] Responsives Design (Frontend)
- [x] Clean Code (PEP8, Logging statt print, kurze Funktionen)
- [x] Umfangreiche Unit-Tests (Happy/Unhappy Path)
- [x] Testausführung & Coverage >80%
- [x] README mit Install, Test, DoD
- [x] GitHub Push

---

## 🧹 Clean Code & Logging
- Keine print-Statements im Code, stattdessen `import logging`
- Funktionen möglichst <14 Zeilen, Single Responsibility
- Aussagekräftige Namen, keine Magic Numbers
- Kommentare & Docstrings für alle wichtigen Funktionen

---

## 🛠️ Troubleshooting (Kurz)
- **Docker-Fehler:** Docker Desktop läuft?
- **Migrationsfehler:**
  ```bash
  docker-compose exec web python manage.py makemigrations
  docker-compose exec web python manage.py migrate
  ```
- **Superuser:** Wird automatisch per `.env` angelegt (siehe `backend.entrypoint.sh`)

---

## ⚡️ Email Verification in Development/Testing

- In development mode (`DEBUG=True`), all newly registered users are automatically marked as email-verified.
- No email verification token is created and no verification email is sent in this mode.
- This ensures you can log in directly after registration (e.g. for Postman, frontend, or mentor testing) without manual email confirmation.
- In production (`DEBUG=False`), users must verify their email via the link sent to their inbox.

---

## 📄 Hinweise
- Alle Umgebungsvariablen in `.env` pflegen
- Testdatenbank/Settings für lokale Tests ggf. auf SQLite anpassen
- Für lokale Tests: pytest kann mit SQLite laufen, wenn in `settings.py` entsprechend konfiguriert

---

**Built with ❤️ for Developer Akademie**
