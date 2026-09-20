# 🎙️ Live Chinese to English Subtitles (PWA)

A real-time, low-latency Chinese to English speech-to-text translation application powered by **Google Gemini Live API** (`gemini-3.5-live-translate-preview`).

---

## 🌐 Live 24/7 Web App
- **Live URL**: [https://gbraun94.github.io/live-subtitles/](https://gbraun94.github.io/live-subtitles/)
- **GitHub Repository**: [https://github.com/gbraun94/live-subtitles](https://github.com/gbraun94/live-subtitles)

---

## ✨ Features

- **Natural Flowing Sentences**: Continuous sentence joiner formats speech into complete, readable English paragraphs instead of fragmented word bubbles.
- **Progressive Web App (PWA)**: Installable directly to phone home screen with dedicated app icon and full-screen native view.
- **Silent Subtitle Mode**: Dedicated to reading subtitles live on screen without audio feedback.
- **Adjustable Text Size**: `A-` and `A+` controls to enlarge subtitles for comfortable viewing.
- **Zero Server Dependency**: Runs completely client-side in the browser, communicating directly with Gemini over WebSockets.
- **Privacy-First**: Gemini API key is stored only in the user's personal device local storage (`localStorage`), never on the server or on GitHub.

---

## 📁 Project Structure

```
live-translator/
├── index.html            # Main web application & UI
├── manifest.json         # PWA configuration for home screen install
├── sw.js                 # Service worker for offline caching & app shell
├── icon-192.png          # App icon (192x192)
├── icon-512.png          # App icon (512x512)
├── server.py             # Optional local development server
└── live_translate_cli.py # Standalone terminal Python translator
```

---

## 🚀 Local Development

To run locally on your computer:
```bash
python3 server.py
# Open http://localhost:8080
```
