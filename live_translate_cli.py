#!/usr/bin/env python3
"""
Terminal CLI Live Audio Translator (Chinese -> English)
Uses Gemini Live Translate API (`gemini-3.5-live-translate-preview`).

Requirements:
  pip install google-genai sounddevice numpy
"""

import asyncio
import os
import sys

def check_dependencies():
    missing = []
    try:
        import sounddevice
    except ImportError:
        missing.append("sounddevice")
    try:
        import numpy
    except ImportError:
        missing.append("numpy")
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        missing.append("google-genai")
        
    if missing:
        print("\n[!] Missing required Python dependencies:")
        print(f"    pip install {' '.join(missing)}\n")
        print("Tip: Alternatively, you can use the web interface without installing any packages:")
        print("    python3 server.py\n")
        sys.exit(1)

def main():
    check_dependencies()
    import numpy as np
    import sounddevice as sd
    from google import genai
    from google.genai import types

    LANGUAGES = {
        "zh-Hant": ("Chinese (Trad.)", "🇹🇼"),
        "zh-Hans": ("Chinese (Simp.)", "🇨🇳"),
        "en": ("English", "🇺🇸"),
        "my": ("Burmese", "🇲🇲"),
        "de": ("German", "🇩🇪"),
        "es": ("Spanish", "🇪🇸"),
        "th": ("Thai", "🇹🇭"),
        "pt-BR": ("Portuguese", "🇧🇷"),
        "ar": ("Arabic", "🇸🇦"),
    }

    import argparse
    parser = argparse.ArgumentParser(description="Live Gemini Audio Translator (Multilingual)")
    parser.add_argument("-t", "--target", choices=list(LANGUAGES.keys()), default="en",
                        help="Target translation language code (default: en)")
    parser.add_argument("-s", "--source", choices=list(LANGUAGES.keys()), default="zh-Hant",
                        help="Source spoken language (informational) (default: zh-Hant)")
    parser.add_argument("-d", "--direction", choices=["zh-to-en", "en-to-zh"], default=None,
                        help="Shortcut for translation direction: 'zh-to-en' or 'en-to-zh'")
    parser.add_argument("--script", choices=["zh-Hant", "zh-Hans"], default="zh-Hant",
                        help="Chinese script when translating to Chinese: 'zh-Hant' or 'zh-Hans'")
    args = parser.parse_args()

    if args.direction == "zh-to-en":
        target_lang = "en"
        source_lang = "zh-Hant"
    elif args.direction == "en-to-zh":
        target_lang = args.script
        source_lang = "en"
    else:
        target_lang = args.target
        source_lang = args.source

    src_label, src_flag = LANGUAGES.get(source_lang, (source_lang, "🌐"))
    tgt_label, tgt_flag = LANGUAGES.get(target_lang, (target_lang, "🌐"))

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("\n[!] GEMINI_API_KEY environment variable not set.")
        print("    Run: export GEMINI_API_KEY='your_api_key_here'\n")
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    model = "gemini-3.5-live-translate-preview"
    
    # 16kHz input audio (mono 16-bit PCM)
    input_sample_rate = 16000
    # 24kHz output audio from Gemini
    output_sample_rate = 24000
    chunk_size = 1600  # 100ms chunks

    config = types.LiveConnectConfig(
        response_modalities=["AUDIO"],
        input_audio_transcription=types.AudioTranscriptionConfig(),
        output_audio_transcription=types.AudioTranscriptionConfig(),
        translation_config=types.TranslationConfig(
            target_language_code=target_lang,
            echo_target_language=False
        )
    )

    audio_out_stream = sd.OutputStream(
        samplerate=output_sample_rate,
        channels=1,
        dtype='int16'
    )
    audio_out_stream.start()

    async def send_mic_audio(session):
        loop = asyncio.get_running_loop()
        audio_queue = asyncio.Queue()

        def mic_callback(indata, frames, time, status):
            if status:
                print(status, file=sys.stderr)
            loop.call_soon_threadsafe(audio_queue.put_nowait, indata.copy())

        with sd.InputStream(samplerate=input_sample_rate, channels=1, dtype='int16', blocksize=chunk_size, callback=mic_callback):
            while True:
                chunk = await audio_queue.get()
                pcm_bytes = chunk.tobytes()
                await session.send_realtime_input(
                    audio=types.Blob(
                        data=pcm_bytes,
                        mime_type="audio/pcm;rate=16000"
                    )
                )

    async def receive_translation(session):
        print("\n" + "=" * 60)
        print(f" 🎙️  Listening to {src_label}... Speak into your microphone!")
        print(f" 🔊 {tgt_label} translation will play through your speakers.")
        print(" Press Ctrl+C to stop.")
        print("=" * 60 + "\n")

        async for response in session.receive():
            if not response.server_content:
                continue
                
            content = response.server_content
            if content.input_transcription and content.input_transcription.text:
                print(f"\r{src_flag} [{src_label}]: {content.input_transcription.text}")
                
            if content.output_transcription and content.output_transcription.text:
                print(f"{tgt_flag} [{tgt_label}]: {content.output_transcription.text}\n")
                
            if content.model_turn:
                for part in content.model_turn.parts:
                    if part.inline_data and part.inline_data.data:
                        audio_chunk = np.frombuffer(part.inline_data.data, dtype=np.int16)
                        audio_out_stream.write(audio_chunk)

    async def run_session():
        async with client.aio.live.connect(model=model, config=config) as session:
            await asyncio.gather(
                send_mic_audio(session),
                receive_translation(session)
            )

    try:
        asyncio.run(run_session())
    except KeyboardInterrupt:
        print("\nTranslation stopped.")
    finally:
        audio_out_stream.stop()
        audio_out_stream.close()

if __name__ == "__main__":
    main()
