import http.server
import json
import os
from urllib.parse import urlparse


class CustomHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args,
                 upload_handler=None,
                 command_handler=None,
                 **kwargs):
        self.upload_handler = upload_handler
        self.command_handler = command_handler
        super().__init__(*args, **kwargs)

    def do_PUT(self):
        """Handles file uploads."""
        file_name = os.path.basename(urlparse(self.path).path)
        if not file_name:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing file name in URL.")
            return

        response_code, response_message = self.upload_handler.handle_upload(
            file_stream=self.rfile,
            file_name=file_name,
            headers=self.headers,
        )
        self.send_response(response_code)
        self.end_headers()
        self.wfile.write(response_message.encode())

    def do_POST(self):
        """Handles JSON messages."""
        content_type = self.headers.get('Content-Type')
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode()

        if content_type == "application/json":
            try:
                data = json.loads(body)
                if "command" in data:
                    response = self.command_handler.execute_command(
                        data["command"])
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
        else:
            self.send_response(415)
            self.end_headers()
            self.wfile.write(b"Unsupported Content-Type.")

    def log_message(self, format, *args):
        """Override to suppress default console output."""
        return
