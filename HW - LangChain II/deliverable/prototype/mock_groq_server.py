#!/usr/bin/env python3
"""Minimal local mock server for GROQ endpoint.

Run this in the prototype folder and point `GROQ_ENDPOINT` to
`http://localhost:8000/v1` to test the prototype without external network access.

This server implements `POST /v1/chat/completions` and returns a canned
OpenAI-style response.
"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, obj, status=200):
        data = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        if self.path != "/v1/chat/completions":
            self._send_json({"error": "not found"}, status=404)
            return
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        try:
            payload = json.loads(body)
        except Exception:
            self._send_json({"error": "invalid json"}, status=400)
            return

        # Extract a user message if present
        messages = payload.get("messages") or []
        user_text = None
        for m in messages:
            if m.get("role") == "user":
                user_text = m.get("content")
                break

        # Simple canned reply: echo the question in a sentence
        if user_text:
            reply = f"(mock) The capital of France is Paris. (You asked: {user_text})"
        else:
            reply = "(mock) Hello from the mock GROQ server."

        resp = {
            "id": "mock-1",
            "object": "chat.completion",
            "choices": [
                {"index": 0, "message": {"role": "assistant", "content": reply}}
            ],
        }
        self._send_json(resp)


def run(port=8000):
    server = HTTPServer(("127.0.0.1", port), Handler)
    print(f"Mock GROQ server running at http://127.0.0.1:{port}/v1/chat/completions")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down")
        server.server_close()


if __name__ == "__main__":
    run()
