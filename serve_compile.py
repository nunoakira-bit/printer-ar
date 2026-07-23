# -*- coding: utf-8 -*-
"""Servidor de apoio para compilar o targets.mind pelo navegador.

Serve a pasta printer-ar/ e aceita POST /save para gravar o .mind em disco --
o compilador do MindAR so roda no navegador, entao a pagina compila e devolve
o buffer por aqui.
"""
import http.server, os, sys

ROOT = r"D:\Aplicativos locais Printer\printer-ar"
SAVE_TO = os.path.join(ROOT, "assets", "eco", "targets.mind")
PORT = 8793


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def do_POST(self):
        if self.path != "/save":
            self.send_error(404)
            return
        n = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(n)
        with open(SAVE_TO, "wb") as f:
            f.write(data)
        print(f"GRAVADO {SAVE_TO} ({len(data)} bytes)", flush=True)
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(f"ok {len(data)}".encode())

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, *a):
        pass


print(f"servindo {ROOT} em http://localhost:{PORT}", flush=True)
http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
