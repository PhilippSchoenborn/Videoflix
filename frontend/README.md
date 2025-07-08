# Videoflix – Frontend

## 🚀 Quickstart

1. **Abhängigkeiten installieren**
   ```bash
   npm install
   # oder
   yarn install
   ```
2. **Entwicklungsserver starten**
   ```bash
   npm run dev
   # oder
   yarn dev
   ```
   Die App läuft dann auf http://localhost:5173

3. **Build für Produktion**
   ```bash
   npm run build
   # oder
   yarn build
   ```

## 🔗 API-Anbindung
- Das Frontend kommuniziert mit dem Django-Backend über eine REST-API (Standard: http://localhost:8000/api/)
- Die API-URL kann ggf. in den Umgebungsvariablen angepasst werden.

## 🖥️ Features
- Benutzerregistrierung & Login mit E-Mail-Bestätigung
- Passwort-Reset per E-Mail
- Video-Dashboard mit Genres, Thumbnails und Hero-Video
- Videoplayer mit Qualitätswahl, Fortschritt speichern, Toast-Nachrichten
- Responsive UI für Desktop, Tablet und Mobile
- Rechtliche Seiten (Impressum, Datenschutz) im Footer

## 🧪 Testing
- Linting: `npm run lint`
- Unit-Tests (optional): `npm run test`

## 📄 Hinweise
- Für die volle Funktionalität muss das Backend laufen (siehe Backend-README)
- API-URL ggf. in der Konfiguration anpassen

**Built with ❤️ for Developer Akademie**
