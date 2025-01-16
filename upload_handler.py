import os

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def handle_upload(file_stream, file_name, headers):
    """Handles the logic for uploading a file."""
    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    try:
        content_length = int(headers['Content-Length'])
        with open(file_path, 'wb') as file:
            file.write(file_stream.read(content_length))

        return 201, "File uploaded successfully."
    except Exception as e:
        return 500, f"Error: {str(e)}"

