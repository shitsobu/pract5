import json
import os
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

DATA_DIR = os.environ.get("DATA_DIR", "/data")
STATE_FILE = os.path.join(DATA_DIR, "state.json")
MESSAGE = os.environ.get("MESSAGE", "Attendance online")
APP_VERSION = os.environ.get("APP_VERSION", "1.0")
LOCK = threading.Lock()

# Фиксированные данные посещаемости
STUDENTS = [
    {"name": "Student A", "present": True},
    {"name": "Student B", "present": True},
    {"name": "Student C", "present": False},
    {"name": "Student D", "present": True},
    {"name": "Student E", "present": False},
]


def increment_counter():
    """Увеличивает счетчик запросов в /data/state.json (атомарная запись)."""
    with LOCK:
        count = 0
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                count = int(json.load(f)["requests"])
        except FileNotFoundError:
            pass
        except (ValueError, KeyError, TypeError) as exc:
            print(f"WARNING: state.json повреждён ({exc}), счетчик сброшен", flush=True)
        count += 1
        tmp = STATE_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump({"requests": count}, f)
        os.replace(tmp, STATE_FILE)
        return count


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == "/health":
            self._send(200, {"status": "ok"})
        elif path == "/attendance":
            try:
                count = increment_counter()
            except OSError as exc:
                self._send(500, {"error": f"cannot write state: {exc}"})
                return
            self._send(200, {
                "message": MESSAGE,
                "version": APP_VERSION,
                "present": sum(s["present"] for s in STUDENTS),
                "total": len(STUDENTS),
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "requests": count,
            })
        else:
            self._send(404, {"error": "not found"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8006"))
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"Listening on 0.0.0.0:{port}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
