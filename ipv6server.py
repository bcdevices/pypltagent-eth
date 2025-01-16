#!/usr/bin/env python3
import http.server
import json
import xml.etree.ElementTree as ET
import os
from urllib.parse import urlparse
from command_handler import execute_command
from upload_handler import handle_upload


class CustomHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_PUT(self):
        """Handles file uploads."""
        file_name = os.path.basename(urlparse(self.path).path)
        if not file_name:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing file name in URL.")
            return

        response_code, response_message = handle_upload(self.rfile,
                                                        file_name,
                                                        self.headers)
        self.send_response(response_code)
        self.end_headers()
        self.wfile.write(response_message.encode())

    def do_POST(self):
        """Handles JSON/XML messages."""
        content_type = self.headers.get('Content-Type')
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode()

        if content_type == "application/json":
            try:
                data = json.loads(body)
                if "command" in data:
                    response = execute_command(data["command"])
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode())
                else:
                    self.send_response(200)
                    self.end_headers()
                    response = {"message": "JSON received", "data": data}
                    self.wfile.write(json.dumps(response).encode())
            except json.JSONDecodeError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid JSON.")
        elif content_type == "application/xml":
            try:
                root = ET.fromstring(body)
                self.send_response(200)
                self.end_headers()
                response = {"message": "XML received", "root_tag": root.tag}
                self.wfile.write(json.dumps(response).encode())
            except ET.ParseError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid XML.")
        else:
            self.send_response(415)
            self.end_headers()
            self.wfile.write(b"Unsupported Content-Type.")

    def log_message(self, format, *args):
        """Override to suppress default console output."""
        return


if __name__ == "__main__":
    import socketserver
    import socket

    HOST = "::"  # Listen on all interfaces for IPv6
    PORT = 8080

    class IPv6TCPServer(socketserver.TCPServer):
        address_family = socket.AF_INET6

    with IPv6TCPServer((HOST, PORT), CustomHTTPRequestHandler) as server:
        print(f"Server running at http://[{HOST}]:{PORT}/")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
            server.shutdown()
