import http.server
import ssl
import sys


class MockServer(http.server.BaseHTTPRequestHandler):
    """A stupid request handler"""

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello world!")


def launch_server(port):
    """Launch an (unsafe) HTTPS server"""
    # setup SSL for this server
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('certificate.pem', 'key.pem')

    # prepare a vanilla HTTP server
    server_address = ('0.0.0.0', port)
    httpd = http.server.HTTPServer(server_address, MockServer)

    # wrap the socket with SSL
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    print(f"Starting HTTPS server on port {port}")
    httpd.serve_forever()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 54321
    launch_server(port)