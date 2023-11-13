import requests
import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('Anexos/backend/config/.env')
load_dotenv(dotenv_path=dotenv_path)

tenant_id = os.getenv("TENANT_ID")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
scope = "https://graph.microsoft.com/.default"
grant_type = "client_credentials"

token_data = {
    'grant_type': grant_type,
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': scope
}

token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
token_r = requests.post(token_url, data=token_data)
token = token_r.json().get('access_token')

# Crear el usuario en Azure AD B2C usando Microsoft Graph
graph_url = "https://graph.microsoft.com/v1.0/users"
user_data = {
    "accountEnabled": True,
    "displayName": "Nombre de otro Usuario",
    "mailNickname": "OtroNikcname",
    "userPrincipalName": "usuarioprueba2@facenlearn2.onmicrosoft.com",
    "passwordProfile": {
        "forceChangePasswordNextSignIn": False,
        "password": "ComplexPa$$w0rd!"
    }
}

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

user_r = requests.post(graph_url, headers=headers, json=user_data)

# Verifica si la solicitud fue exitosa
if user_r.status_code == 201:
    print("Usuario creado con éxito.")
    # Puedes obtener más información del cuerpo de la respuesta si es necesario
    user_info = user_r.json()
    print(user_info)
else:
    print("Error al crear el usuario.")
    # Imprime la respuesta que podría contener la razón del error
    print(user_r.text)