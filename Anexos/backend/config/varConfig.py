from dotenv import load_dotenv
import os

# Carga las variables de entorno desde el archivo .env en el mismo directorio
load_dotenv('.env')  # load_dotenv() por defecto busca .env en el directorio actual

# Variables de configuración de Microsoft Azure AD B2C
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TOKEN_ENDPOINT = os.getenv("TOKEN_ENDPOINT")
AUTHORITY_URL = os.getenv("AUTHORITY_URL")

# Configuración de Azure SQL
AZURE_SQL_CONNECTION_STRING = os.getenv("AZURE_SQL_CONNECTION_STRING")

# Configuración de Azure Blob Storage
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_STORAGE_CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER_NAME")