"""
Mini proxy local para el Analizador de Archivos.

Por qué existe: el navegador bloquea (CORS) que una página llame directo a
VirusTotal. Este script hace de puente: sirve el HTML y reenvía cada pedido a
/api/v3/... hacia VirusTotal desde Python, donde esa restricción no existe.

Uso:  python proxy.py   ->  abrir http://localhost:8000
Solo usa la librería estándar de Python y solo escucha en tu propia PC.
"""
import json
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PUERTO = 8000
VIRUSTOTAL = "https://www.virustotal.com"
CARPETA = Path(__file__).parent


def buscar_html():
    """Busca el HTML de la app en esta carpeta, aunque se haya descargado con otro nombre."""
    preferido = CARPETA / "index.html"
    if preferido.exists():
        return preferido
    otros = sorted(CARPETA.glob("*.html"))
    return otros[0] if otros else None


class Proxy(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/api/v3/"):
            return self.reenviar()
        if self.path in ("/", "/index.html"):
            html = buscar_html()
            if html is None:  # no hay ningún .html junto a proxy.py
                aviso = "No encuentro el HTML de la app. Ponelo en la misma carpeta que proxy.py."
                return self.responder(404, "text/plain; charset=utf-8", aviso.encode())
            return self.responder(200, "text/html; charset=utf-8", html.read_bytes())
        self.responder(404, "text/plain", b"No encontrado")

    def do_POST(self):
        if self.path.startswith("/api/v3/"):
            return self.reenviar()
        self.responder(404, "text/plain", b"No encontrado")

    def reenviar(self):
        """Copia el pedido del navegador y lo manda a VirusTotal tal cual."""
        largo = int(self.headers.get("Content-Length", 0))
        cuerpo = self.rfile.read(largo) if largo else None
        cabeceras = {
            "x-apikey": self.headers.get("x-apikey", ""),
            "accept": "application/json",
            "User-Agent": "AnalizadorDeArchivos/1.0",
        }
        if self.headers.get("Content-Type"):  # necesario para subir archivos
            cabeceras["Content-Type"] = self.headers["Content-Type"]

        pedido = urllib.request.Request(VIRUSTOTAL + self.path, data=cuerpo,
                                        headers=cabeceras, method=self.command)
        try:
            with urllib.request.urlopen(pedido, timeout=120) as r:
                self.responder(r.status, r.headers.get("Content-Type", "application/json"), r.read())
        except urllib.error.HTTPError as e:  # 404, 401, 429...: se pasan al navegador
            codigo = e.code
            # "Archivo no encontrado" es una respuesta normal (VirusTotal no lo conoce todavía),
            # pero el navegador pinta todo 404 en rojo en la consola. Lo mandamos como 200.
            if codigo == 404 and self.command == "GET" and self.path.startswith("/api/v3/files/"):
                codigo = 200
            self.responder(codigo, e.headers.get("Content-Type", "application/json"), e.read())
        except urllib.error.URLError as e:   # sin internet, DNS, etc.
            error = {"error": {"message": f"Sin conexión con VirusTotal: {e.reason}"}}
            self.responder(502, "application/json", json.dumps(error).encode())

    def responder(self, codigo, tipo, cuerpo):
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)


if __name__ == "__main__":
    html = buscar_html()
    if html:
        print(f"Usando {html.name}")
    else:
        print(f"OJO: no hay ningún archivo .html en {CARPETA}")
    print(f"Abrí http://localhost:{PUERTO} en el navegador (Ctrl+C para cerrar)")
    ThreadingHTTPServer(("127.0.0.1", PUERTO), Proxy).serve_forever()
