import requests
import os
from dotenv import load_dotenv
from pathlib import Path

class AzureADManager:
    def __init__(self):
        # Carga las variables de entorno
        dotenv_path = Path('Anexos/backend/.env')
        load_dotenv(dotenv_path=dotenv_path)
        self.tenant_id = os.getenv("TENANT_ID")
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.scope = "https://graph.microsoft.com/.default"
        self.grant_type = "client_credentials"
        self.token_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        self.graph_url = "https://graph.microsoft.com/v1.0/users"

    def get_token(self):
        token_data = {
            'grant_type': self.grant_type,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': self.scope
        }
        response = requests.post(self.token_url, data=token_data)
        # Lanza una excepción si la solicitud no fue exitosa
        response.raise_for_status()  
        return response.json().get('access_token')

    def register_user(self, user_data):
        token = self.get_token()
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        response = requests.post(self.graph_url, headers=headers, json=user_data)
        return response

    def update_user(self, user_id, update_data):
        token = self.get_token()
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        user_url = f"{self.graph_url}/{user_id}"
        response = requests.patch(user_url, headers=headers, json=update_data)
        return response

    def delete_user(self, user_id):
        token = self.get_token()
        headers = {
            'Authorization': f'Bearer {token}'
        }
        user_url = f"{self.graph_url}/{user_id}"
        response = requests.delete(user_url, headers=headers)
        return response
