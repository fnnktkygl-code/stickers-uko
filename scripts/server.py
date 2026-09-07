import http.server
import socketserver
import threading
import os
import sys

class DualServerHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def log_message(self, format, *args):
        # Keep logs clean
        pass

DualServerHandler.extensions_map.update({
    '.webp': 'image/webp',
    '.png': 'image/png',
    '.gif': 'image/gif',
    '.mp4': 'video/mp4',
    '.json': 'application/json',
    '.js': 'application/javascript',
    '.css': 'text/css',
    '.html': 'text/html'
})

def run_on_port(port):
    try:
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("", port), DualServerHandler) as httpd:
            print(f"🚀 Server listening on http://localhost:{port}")
            httpd.serve_forever()
    except Exception as e:
        print(f"Port {port} failed: {e}")

if __name__ == "__main__":
    ports = [3000, 8080]
    threads = []
    for p in ports:
        t = threading.Thread(target=run_on_port, args=(p,), daemon=False)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
