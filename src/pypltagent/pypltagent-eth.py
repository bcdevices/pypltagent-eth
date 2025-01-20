#!/usr/bin/env python3
from ipv6server import IPv6TCPServer
from custom_http_handler import CustomHTTPRequestHandler
from upload_handler import UploadHandler
from command_handler import CommandHandler
import argparse


def main():
    parser = argparse.ArgumentParser(description="pypltagent-eth")
    parser.add_argument(
        "--host", default="::", help="The host to listen on (default: '::')"
    )
    parser.add_argument(
        "--port", type=int, default=8080,
        help="The port to listen on (default: 8080)"
    )
    parser.add_argument(
        "--upload-folder",
        default="uploads",
        help="The folder to save uploaded files (default: 'uploads')",
    )
    args = parser.parse_args()

    upload_handler = UploadHandler(upload_folder=args.upload_folder)
    command_handler = CommandHandler()

    with IPv6TCPServer(
        (args.host, args.port),
        lambda *args, **kwargs: CustomHTTPRequestHandler(
            *args,
            upload_handler=upload_handler,
            command_handler=command_handler, **kwargs
        ),
    ) as server:
        print(f"Server running at http://[{args.host}]:{args.port}/")
        print(f"Uploads will be saved to: {args.upload_folder}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
            server.shutdown()


if __name__ == "__main__":
    main()
