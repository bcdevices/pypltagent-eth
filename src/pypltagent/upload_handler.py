import os


class UploadHandler:
    def __init__(self, upload_folder="uploads"):
        self.upload_folder = upload_folder
        os.makedirs(self.upload_folder, exist_ok=True)

    def handle_upload(self, file_stream, file_name, headers):
        """Handles the logic for uploading a file."""
        file_path = os.path.join(self.upload_folder, file_name)
        try:
            content_length = int(headers['Content-Length'])
            with open(file_path, 'wb') as file:
                file.write(file_stream.read(content_length))

            return 201, "File uploaded successfully."
        except Exception as e:
            return 500, f"Error: {str(e)}"
