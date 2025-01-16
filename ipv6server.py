#!/usr/bin/env python3
from custom_http_handler import CustomHTTPRequestHandler
import socketserver
import socket

HOST = "::"  # Listen on all interfaces for IPv6
PORT = 8080


class IPv6TCPServer(socketserver.TCPServer):
    address_family = socket.AF_INET6


if __name__ == "__main__":
    with IPv6TCPServer((HOST, PORT), CustomHTTPRequestHandler) as server:
        print(f"Server running at http://[{HOST}]:{PORT}/")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
            server.shutdown()
