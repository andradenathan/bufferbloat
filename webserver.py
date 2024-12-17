import http.server
import socketserver
import os

PORT = 8080 

current_dir = os.path.dirname(os.path.abspath(__file__))

os.chdir(current_dir)

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Servidor rodando na porta {PORT}")
    print(f"Acesse: http://localhost:{PORT}/index.html")
    httpd.serve_forever()
