#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
로컬 미리보기 서버

Cloudflare Pages와 같은 방식으로 주소를 처리합니다.
  /brand      -> brand.html 을 그대로 보여줍니다
  /brand.html -> /brand 으로 308 이동합니다
  없는 주소   -> 404.html 을 보여줍니다

사용법:
    python3 tools/serve.py
    브라우저에서 http://localhost:8080 접속

파일을 그냥 더블클릭해서 열면 /brand 같은 주소가 동작하지 않습니다.
확인은 반드시 이 서버나 `npx wrangler pages dev .` 로 해 주세요.
"""
import http.server
import os
import socketserver
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080


class PagesHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def do_GET(self):
        path = self.path.split("?")[0]

        # .html 로 들어오면 확장자를 뗀 주소로 이동 (Cloudflare 기본 동작)
        if path.endswith(".html") and path != "/404.html":
            target = "/" if path == "/index.html" else path[:-5]
            self.send_response(308)
            self.send_header("Location", target)
            self.end_headers()
            return

        super().do_GET()

    def translate_path(self, path):
        result = super().translate_path(path)
        if os.path.isdir(result):
            index = os.path.join(result, "index.html")
            if os.path.exists(index):
                return index
        if not os.path.exists(result) and not os.path.splitext(result)[1]:
            candidate = result + ".html"
            if os.path.exists(candidate):
                return candidate
        return result

    def send_error(self, code, message=None, explain=None):
        if code == 404:
            page = os.path.join(ROOT, "404.html")
            if os.path.exists(page):
                body = open(page, "rb").read()
                self.send_response(404)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
        super().send_error(code, message, explain)

    def log_message(self, fmt, *args):
        sys.stderr.write("  %s\n" % (fmt % args))


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), PagesHandler) as httpd:
        print(f"\n오렌지 마켓 미리보기 → http://localhost:{PORT}")
        print("종료하려면 Ctrl+C\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n종료했습니다.")
