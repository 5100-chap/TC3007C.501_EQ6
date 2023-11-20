from azure.storage.blob import BlobServiceClient
from config import varConfig
import time
from azure.core.exceptions import AzureError

class BlobManager:
    def __init__(self):
        self.connection_string = varConfig.AZURE_STORAGE_CONNECTION_STRING
        self.container_name = varConfig.AZURE_STORAGE_CONTAINER_NAME
        self.service_client = self.connect_to_blob_storage_with_retry()

    def connect_to_blob_storage_with_retry(self):
        max_retries = 4
        retry_delay = 7  # segundos

        for retry in range(max_retries):
            try:
                # Intenta conectarte a Blob Storage
                blob_service_client = BlobServiceClient.from_connection_string(varConfig.AZURE_STORAGE_CONNECTION_STRING)
                return blob_service_client
            except AzureError as ex:
                print(f"Error al conectar a Blob Storage. Intento {retry+1}/{max_retries}")
                print(f"Detalles del error: {ex}")
                if retry < max_retries - 1:
                    print(f"Reintentando en {retry_delay} segundos...")
                    time.sleep(retry_delay)
        
        # Si todos los intentos fallan, lanza una excepción
        raise Exception("No se pudo conectar a Blob Storage después de varios intentos")
    
    def upload_image(self, image_data, file_name):
        blob_client = self.service_client.get_blob_client(container=self.container_name, blob=file_name)
        blob_client.upload_blob(image_data, overwrite=True)
        image_url = f"https://{varConfig.AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net/{self.container_name}/{file_name}"
        return image_url
    
    def delete_image(self, image_url):
        blob_name = image_url.split('/')[-1]
        blob_client = self.service_client.get_blob_client(container=self.container_name, blob=blob_name)
        try:
            blob_client.delete_blob()
            print("Archivo borrado exitosamente.")
        except AzureError as ex:
            raise Exception(f"No se pudo borrar el archivo. Detalles del error: {ex}")
