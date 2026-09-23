"""Chạy: python python/app.py [--port 8000] [--no-browser].

Máy chủ cục bộ cho một người học. Không triển khai lên Internet.
Giao diện ở ../web; toàn bộ thuật toán chạy trong Python, không chạy trong JavaScript.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import secrets
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from dich_vu import UngDung

WEB = Path(__file__).resolve().parent.parent / "web"
STATIC = {"/": ("index.html", "text/html; charset=utf-8"),
          "/style.css": ("style.css", "text/css; charset=utf-8"),
          "/app.js": ("app.js", "text/javascript; charset=utf-8")}


class MayChu(ThreadingHTTPServer):
    daemon_threads = True
    def __init__(self, address):
        super().__init__(address, XuLy)
        self.ung_dung = UngDung()
        self.khoa = threading.Lock()
        self.token = secrets.token_urlsafe(32)
        self.origins = {f"http://127.0.0.1:{self.server_port}", f"http://localhost:{self.server_port}"}
        self.hosts = {f"127.0.0.1:{self.server_port}", f"localhost:{self.server_port}"}


class XuLy(BaseHTTPRequestHandler):
    def log_message(self, *args) -> None:
        pass  # Tránh in dữ liệu người dùng vào terminal.

    def gui(self, code: int, body: bytes, mime: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'")
        self.end_headers()
        self.wfile.write(body)

    def json(self, code: int, value: dict) -> None:
        self.gui(code, json.dumps(value, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

    def hop_le(self) -> bool:
        return self.headers.get("Host", "") in self.server.hosts

    def do_GET(self) -> None:
        if not self.hop_le():
            return self.json(403, {"ok": False, "message": "Host không hợp lệ."})
        path = self.path.split("?", 1)[0]
        if path == "/api/state":
            with self.server.khoa:
                state = self.server.ung_dung.trang_thai()
            return self.json(200, {"ok": True, "state": state, "token": self.server.token})
        if path == "/favicon.ico":
            return self.gui(204, b"", "image/x-icon")
        if path in STATIC:
            name, mime = STATIC[path]
            return self.gui(200, (WEB / name).read_bytes(), mime)
        self.json(404, {"ok": False, "message": "Không tìm thấy đường dẫn."})

    def do_POST(self) -> None:
        if (not self.hop_le() or self.headers.get("Origin") not in self.server.origins
                or self.headers.get("X-Lab-Token") != self.server.token):
            return self.json(403, {"ok": False, "message": "Tải lại trang từ địa chỉ máy chủ cục bộ."})
        if self.path != "/api/action":
            return self.json(404, {"ok": False, "message": "Không có API này."})
        if self.headers.get("Content-Type", "").split(";")[0] != "application/json":
            return self.json(415, {"ok": False, "message": "Cần dữ liệu JSON."})
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 1 <= size <= 16384:
                raise ValueError("Kích thước yêu cầu không hợp lệ.")
            self.connection.settimeout(10)
            data = json.loads(self.rfile.read(size).decode("utf-8"))
            with self.server.khoa:
                response = self.server.ung_dung.thuc_hien(data)
            self.json(200, response)
        except NotImplementedError as exc:
            self.json(422, {"ok": False, "message": str(exc)})
        except (ValueError, TypeError, UnicodeError) as exc:
            self.json(400, {"ok": False, "message": str(exc)})
        except Exception as exc:
            self.json(500, {"ok": False, "message": f"Lỗi trong mã: {type(exc).__name__}. Kiểm tra hàm vừa sửa và chạy bộ kiểm thử."})


def main() -> None:
    parser = argparse.ArgumentParser(description="Thực hành Chương 5 trên máy cá nhân")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()
    if not 1024 <= args.port <= 65535:
        parser.error("Cổng phải nằm trong khoảng 1024..65535.")
    if not (WEB / "index.html").is_file():
        parser.error("Thiếu thư mục web. Cần giải nén toàn bộ gói, không chỉ riêng app.py.")
    try:
        server = MayChu(("127.0.0.1", args.port))
    except OSError as exc:
        parser.exit(1, f"Không mở được cổng {args.port}: {exc}. Thử --port 8002.\n")
    url = f"http://127.0.0.1:{args.port}"
    print(f"Python: {url}\nGiữ cửa sổ này mở. Dừng bằng Ctrl+C.", flush=True)
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nĐã dừng máy chủ.")
    finally:
        server.server_close()

if __name__ == "__main__":
    main()
