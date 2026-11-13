from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import hashlib
import json
import os

ENGINE_PATH = os.environ.get(
    "ENGINE_PATH", "/app/models/eo_detector_fp16.engine"
)
MANIFEST_PATH = os.environ.get(
    "MANIFEST_PATH", "/app/models/manifest.json"
)
WORKER_PORT = int(os.environ.get("WORKER_PORT", "9000"))


def calculate_sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as engine:
        for chunk in iter(lambda: engine.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_engine():
    try:
        with open(MANIFEST_PATH, "r", encoding="utf-8") as file:
            manifest = json.load(file)

        expected = manifest.get("sha256", "").lower()
        actual = calculate_sha256(ENGINE_PATH)

        valid = bool(expected) and actual == expected
        return valid, {
            "engine_loaded": valid,
            "checksum_valid": valid,
            "model_name": manifest.get("model_name"),
            "version": manifest.get("version"),
            "actual_sha256": actual,
        }

    except (OSError, ValueError, TypeError, AttributeError) as error:
        return False, {
            "engine_loaded": False,
            "checksum_valid": False,
            "error": str(error),
        }


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path != "/status":
            self.send_json(404, {"error": "not found"})
            return

        valid, result = validate_engine()
        self.send_json(200 if valid else 503, result)

    def log_message(self, fmt, *args):
        print(fmt % args, flush=True)


if __name__ == "__main__":
    print(f"Starting inference worker on port {WORKER_PORT}", flush=True)
    ThreadingHTTPServer(
        ("0.0.0.0", WORKER_PORT), Handler
    ).serve_forever()
