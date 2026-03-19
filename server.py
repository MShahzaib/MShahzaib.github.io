import os
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler


class Handler(SimpleHTTPRequestHandler):
    def _serve_wasm(self, send_body: bool):
        if self.path != "/ruby-demo.wasm":
            self.send_error(404, "Not found")
            return

        try:
            with open("ruby-demo.wasm.br", "rb") as f:
                data = f.read()
        except FileNotFoundError:
            self.send_error(404, "ruby-demo.wasm.br not found")
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/wasm")
        self.send_header("Content-Encoding", "br")
        self.send_header("Cache-Control", "public, max-age=604800, immutable")
        self.send_header("Vary", "Accept-Encoding")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()

        if send_body:
            self.wfile.write(data)

    def do_GET(self):
        self._serve_wasm(send_body=True)

    def do_HEAD(self):
        self._serve_wasm(send_body=False)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, HEAD, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"Serving on http://127.0.0.1:{port}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()