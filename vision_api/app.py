from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import urllib.request
from urllib.error import URLError, HTTPError

WORKER_URL = os.environ.get(
    "WORKER_URL", "http://inference_worker:9000"
).rstrip("/")
APP_PORT = int(os.environ.get("APP_PORT", "8000"))


def check_worker():
    try:
        request = urllib.request.Request(f"{WORKER_URL}/status")
        with urllib.request.urlopen(request, timeout=2) as response:
            if response.status != 200:
                return False
            data = json.loads(response.read().decode("utf-8"))
            return (
                data.get("engine_loaded") is True
                and data.get("checksum_valid") is True
            )
    except (URLError, HTTPError, TimeoutError, OSError, ValueError):
        return False


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            ready = check_worker()
            self.send_json(
                200 if ready else 503,
                {
                    "status": "healthy" if ready else "degraded",
                    "worker_ready": ready,
                },
            )
            return

        if self.path == "/api/v1/detect":
            if not check_worker():
                self.send_json(
                    503,
                    {"error": "Inference worker unavailable or engine invalid"},
                )
                return

            # Challenge simulation only: this is not TensorRT inference.
            self.send_json(
                200,
                {
                    "stream": "EO_CAM_01",
                    "detections": [
                        {"cls": "vehicle", "conf": 0.91}
                    ],
                },
            )
            return

        self.send_json(404, {"error": "not found"})

    def log_message(self, fmt, *args):
        print(fmt % args, flush=True)


if __name__ == "__main__":
    print(
        f"Starting vision API on port {APP_PORT}; worker={WORKER_URL}",
        flush=True,
    )
    ThreadingHTTPServer(
        ("0.0.0.0", APP_PORT), Handler
    ).serve_forever()
