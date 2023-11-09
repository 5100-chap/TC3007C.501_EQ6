from azure.storage.blob import BlobServiceClient
from config import varConfig

class BlobManager:
    def __init__(self):
        self.connection_string = varConfig.AZURE_STORAGE_CONNECTION_STRING
        self.container_name = varConfig.AZURE_STORAGE_CONTAINER_NAME
        self.service_client = BlobServiceClient.from_connection_string(self.connection_string)

    def upload_image(self, image_data, file_name):
        # Lógica para subir imágenes al Blob Storage
        pass

    # Más métodos para manejar Blob Storage
    # ...