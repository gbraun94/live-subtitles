# Live Subtitles (Chinese to English Real-Time Subtitles)

## Project Overview
Real-time spoken Chinese (Traditional/Simplified) to English subtitles Progressive Web App (PWA). Powered by Google Gemini Live bidirectional streaming API (`gemini-3.5-live-translate-preview`). Designed specifically for mobile browser use (Samsung S25 Ultra / Android Chrome) with 24/7 cloud hosting via GitHub Pages.

- **GitHub Repository**: https://github.com/gbraun94/live-subtitles
- **Live Production URL**: https://gbraun94.github.io/live-subtitles/
- **Local Directory**: `/home/gabriel/live-subtitles`

## Architecture & Tech Stack
- **Frontend**: Vanilla JavaScript (zero build step), HTML5, CSS3.
- **Audio Capture**: Web Audio API (`AudioContext`, `AudioWorkletNode` / `ScriptProcessorNode`), downsampled to 16kHz mono PCM (Linear 16-bit).
- **Subtitles Streaming**: Direct WebSocket connection to Gemini Live Multimodal WebSocket API (`wss://generativelanguage.googleapis.com/ws/...`).
- **PWA**: `manifest.json`, `sw.js` (offline caching), app icons (`icon-192.png`, `icon-512.png`).
- **Local Testing Server**: `python3 server.py` (serves directory on `http://0.0.0.0:8080`).

## Key Design Principles
1. **Muted by Default**: The user reads subtitles in real time; voice output is muted by default (`isMuted = true`).
2. **Hidden Chinese Box**: Transcription of the input Chinese is hidden to provide maximal screen space for English subtitles.
3. **Continuous Sentence Flow**: `joinSentences()` connects fragmented audio tokens into smooth, natural paragraphs with punctuation, capitalization, and overlap deduplication.
4. **Local API Key Storage**: The Gemini API key is stored strictly on the client device in `localStorage` (`gemini_live_api_key`) and is never sent to GitHub or any server.
