import requests
from datetime import datetime, timedelta
from config import varConfig

class AzureADManager:
    def __init__(self, db_manager):
        # Carga las variables de entorno
        self.tenant_id = varConfig.TENANT_ID
        self.client_id = varConfig.CLIENT_ID
        self.client_secret = varConfig.CLIENT_SECRET
        self.scope = "https://graph.microsoft.com/.default"
        self.token_url = (
            f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        )
        self.graph_url = "https://graph.microsoft.com/v1.0/users"
        self.token = None
        self.token_expiry = datetime.utcnow()
        self.db_manager = db_manager
        self.grant_type ="client_credentials"

    def get_token(self):
        # Verifica si el token ya está caché y aún es válido
        if self.token and datetime.utcnow() < self.token_expiry:
            return self.token

        # Si no hay token o está expirado, obtiene uno nuevo
        token_data = {
            "grant_type": self.grant_type,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": self.scope,
        }
        response = requests.post(self.token_url, data=token_data)
        response.raise_for_status()
        token_response = response.json()
        self.token = token_response.get("access_token")
        # Asume que el token expira en menos tiempo del que indica el 'expires_in' para tener un margen
        expires_in = token_response.get(
            "expires_in", 3599
        )  # 3599 segundos son 59 minutos y 59 segundos
        self.token_expiry = datetime.utcnow() + timedelta(
            seconds=expires_in - 300
        )  # Resta 5 minutos para el margen
        return self.token

    def make_request(self, method, url, data=None):
        # Obtiene el token y configura los encabezados
        token = self.get_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        # Realiza la solicitud HTTP
        if method == "post":
            response = requests.post(url, headers=headers, json=data)
        elif method == "patch":
            response = requests.patch(url, headers=headers, json=data)
        elif method == "delete":
            response = requests.delete(url, headers=headers)
        else:
            raise ValueError("Método HTTP no soportado")

        response.raise_for_status()
        return response

    def register_user(self, user_id, user_data, user_role):
        # Preparar datos para Azure AD B2C (eliminar 'Rol' si está presente)
        b2c_data = {key: value for key, value in user_data.items() if key != 'Rol'}

        # Registro en Azure AD B2C
        b2c_response = self.make_request("post", self.graph_url, b2c_data)
        if b2c_response.status_code != 201:
            raise Exception("Error al registrar en Azure AD B2C")

        azure_b2c_id = b2c_response.json().get("id")
        user_data["AzureB2C_ID"] = azure_b2c_id

        # Registro en la base de datos
        try:
            self.db_manager.register_user(user_id, user_data, user_role)
        except Exception as e:
            self.delete_user(azure_b2c_id)
            raise e

        return b2c_response


    def update_user(self, user_id, user_data, user_role):
        # Actualiza el usuario en Azure AD B2C
        user_url = f"{self.graph_url}/{user_id}"
        b2c_response = self.make_request("patch", user_url, user_data)

        if b2c_response.status_code == 204:
            # También actualiza el usuario en la base de datos
            self.db_manager.update_user(user_id, user_data, user_role)

        return b2c_response

    def delete_user(self, user_id, user_role):
        # Elimina el usuario de Azure AD B2C
        user_url = f"{self.graph_url}/{user_id}"
        b2c_response = self.make_request("delete", user_url)

        if b2c_response.status_code == 204:
            # También elimina el usuario de la base de datos
            self.db_manager.delete_user(user_id, user_role)

        return b2c_response
