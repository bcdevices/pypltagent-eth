#!/usr/bin/env python3
import argparse
import http.server
import json
import os
import socket
import socketserver
import subprocess
from datetime import datetime
from urllib.parse import urlparse


HOST = "::"
PORT = 8080


class UploadHandler:
    def handle_upload(self, handler):
        """Handles file upload using the handler context."""
        file_name = os.path.basename(urlparse(handler.path).path)
        content_length = int(handler.headers.get("Content-Length", 0))

        if not file_name or content_length <= 0:
            handler.send_response(400)
            handler.end_headers()
            handler.wfile.write(b"Missing file name or Content-Length.")
            return

        file_path = os.path.join("uploads", file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        try:
            # Stream the upload to disk
            with open(file_path, "wb") as file:
                remaining = content_length
                while remaining > 0:
                    chunk = handler.rfile.read(min(8192, remaining))
                    if not chunk:
                        break
                    file.write(chunk)
                    remaining -= len(chunk)

            if remaining > 0:
                handler.send_response(400)
                handler.end_headers()
                handler.wfile.write(b"Incomplete upload.")
                return

            handler.log_request_details(f"INFO: Received {file_name}")
            handler.send_response(201)
            handler.end_headers()
            handler.wfile.write(b"File uploaded successfully.")
        except Exception as e:
            handler.log_request_details(f"ERR: {str(e)}")
            handler.send_response(500)
            handler.end_headers()
            handler.wfile.write(f"Error: {str(e)}".encode())


class CommandHandler:
    def execute_command(self, handler):
        """Executes a command using the handler context."""
        try:
            body = handler.rfile.read(int(handler.headers["Content-Length"])).decode()
            data = json.loads(body)

            if "command" not in data:
                handler.send_response(400)
                handler.end_headers()
                handler.wfile.write(b"Missing 'command' field in JSON.")
                return

            command = data["command"]
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            response = {
                "command": command,
                "retval": result.returncode,
                "stdout": result.stdout.strip().split("\n"),
                "stderr": result.stderr.strip().split("\n"),
                "status": "completed",
                "passFail": "PASS" if result.returncode == 0 else "FAIL",
            }

            handler.send_response(200)
            handler.end_headers()
            handler.wfile.write(json.dumps(response).encode())
        except Exception as e:
            handler.send_response(500)
            handler.end_headers()
            handler.wfile.write(f"Error: {str(e)}".encode())


class CustomHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_PUT(self):
        """Delegate PUT requests to the upload handler."""
        UploadHandler().handle_upload(self)

    def do_POST(self):
        """Delegate POST requests to the command handler."""
        CommandHandler().execute_command(self)

    def log_request_details(self, msg):
        """Logs the request details."""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        client_ip = self.client_address[0]
        user_agent = self.headers.get("User-Agent", "Unknown User-Agent")
        print(f"[{current_time}] {msg} Client IP: {client_ip}, User-Agent: {user_agent}")

    def log_message(self, format, *args):
        """Override to suppress default logging."""
        return


class IPv6TCPServer(socketserver.TCPServer):
    address_family = socket.AF_INET6
    allow_reuse_address = True
    timeout = 300  # 5 minutes

def main():
    parser = argparse.ArgumentParser(description="pypltagent-eth")
    parser.add_argument("--host", default=HOST, help="The host to listen on")
    parser.add_argument("--port", type=int, default=PORT, help="The port to listen on")
    parser.add_argument("--upload-folder", default="uploads", help="Folder for uploads")
    args = parser.parse_args()

    def handler_factory(*handler_args, **handler_kwargs):
        def create_handler(request, client_address, server):
            handler = CustomHTTPRequestHandler(request, client_address, server)
            handler.upload_handler = UploadHandler()
            handler.command_handler = CommandHandler()
            return handler
        return create_handler

    with IPv6TCPServer((args.host, args.port), handler_factory()) as server:
        print(f"Server running at http://[{args.host}]:{args.port}/")
        print(f"Uploads will be saved to: {args.upload_folder}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
            server.shutdown()


if __name__ == "__main__":
    main()
