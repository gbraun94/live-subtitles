#!/usr/bin/env python3
"""
Simple HTTP server for Gemini Live Translator.
Serves the web application and provides API key configuration from environment.
"""

import http.server
import json
import os
import socketserver
import sys
import webbrowser

PORT = int(os.environ.get("PORT", 8080))
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class TranslatorHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path == "/api/config":
            api_key = os.environ.get("GEMINI_API_KEY", "")
            response = {
                "hasEnvKey": bool(api_key),
                "apiKey": api_key,  # Localhost only
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return

        super().do_GET()

    def log_message(self, format, *args):
        # Keep console output clean
        if "/api/config" not in args[0]:
            super().log_message(format, *args)

def main():
    os.chdir(DIRECTORY)
    # Enable address reuse so restarting works immediately
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("0.0.0.0", PORT), TranslatorHandler) as httpd:
        print(f"\n" + "=" * 60)
        print(f"  Gemini Live Translator is running!")
        print(f"  Open in your browser: http://localhost:{PORT}")
        if os.environ.get("GEMINI_API_KEY"):
            print(f"  GEMINI_API_KEY detected in environment.")
        else:
            print(f"  No GEMINI_API_KEY in environment — you can enter it in the web UI.")
        print(f"=" * 60 + "\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")

if __name__ == "__main__":
    main()
