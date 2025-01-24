from google.cloud import storage
from app.core.config import settings
import os

class GoogleCloudStorage:
    def __init__(self):
        self.client = storage.Client.from_service_account_info({
            "type": "service_account",
            "project_id": settings.GCS_PROJECT_ID,
            "private_key": settings.GCS_PRIVATE_KEY.replace("\\n", "\n"),
            "client_email": settings.GCS_CLIENT_EMAIL,
            "client_id": settings.GCS_CLIENT_ID,
            "token_uri": settings.GCS_TOKEN_URI,
        })
        self.bucket = self.client.bucket(settings.GCS_BUCKET_NAME)

    async def upload_file(self, file, destination_path: str):
        blob = self.bucket.blob(destination_path)
        blob.upload_from_file(file)
        return blob.public_url

    async def delete_file(self, file_path: str):
        blob = self.bucket.blob(file_path)
        blob.delete()