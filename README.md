# 🎙️ Gemini Live Translator (Chinese ➔ English)

A real-time, low-latency, speech-to-speech translation application powered by the **Gemini Live API** (`gemini-3.5-live-translate-preview`).

---

## Features

- **Real-Time Speech-to-Speech**: Speak in Chinese and immediately hear the spoken English translation.
- **Live Dual Subtitles**:
  - 🇨🇳 Input transcription of spoken Chinese.
  - 🇺🇸 Output transcription of translated English.
- **Low Latency**: Directly streams 16kHz PCM audio and receives 24kHz audio via WebSockets.
- **Zero Install Web App**: The web app runs in any modern browser with zero dependencies—no Python sound drivers required!
- **Terminal CLI**: Standalone Python script for terminal environments.

---

## Option 1: Web Interface (Recommended)

The Web interface accesses your browser's microphone and audio output directly without needing ALSA or PulseAudio configuration.

### 1. Start the local server
```bash
cd /home/gabriel/.gemini/antigravity-cli/scratch/live-translator
python3 server.py
```

### 2. Open in your browser
Navigate to:
```
http://localhost:8080
```

### 3. Usage
1. Click **Settings** and enter your **Gemini API Key** (or set `export GEMINI_API_KEY="..."` before running `server.py`).
2. Wear headphones (recommended to prevent microphone echo/feedback).
3. Click **Start Translating**.
4. Speak Chinese into your microphone. You will hear the English translation spoken through your speakers while reading live subtitles.

---

## Option 2: Terminal CLI

If you want to run the translator purely in the terminal:

```bash
# 1. Install dependencies
pip install google-genai sounddevice numpy

# 2. Set your API key
export GEMINI_API_KEY="your_api_key_here"

# 3. Run translator
python3 live_translate_cli.py
```

---

## Configuration Options

- **Target Language**: Defaults to `en` (English). Can be changed to `zh` for reverse English-to-Chinese translation.
- **Echo Target Language**:
  - `false` (default): Remains silent when speech is already in the target language.
  - `true`: Repeats speech in the target language.
