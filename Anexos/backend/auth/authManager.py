from flask import session, redirect, url_for, request
import requests
from dotenv import load_dotenv
from pathlib import Path
import os
import urllib.parse

class AuthManager:
    def __init__(self, url):
        # Carga las variables de entorno
        dotenv_path = Path('Anexos/backend/.env')
        load_dotenv(dotenv_path=dotenv_path)

        # Configuración de Azure AD B2C
        self.tenant_id = os.getenv("TENANT_ID")
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.scope = "https://graph.microsoft.com/.default"
        self.grant_type = "client_credentials"
        self.token_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        self.redirect_uri = url + "/login-redirect"  # Asegúrate de cambiar esto a tu URI de redirección registrada
        self.token_endpoint = os.getenv("TOKEN_ENDPOINT")

    def build_auth_url(self):
        # Construye la URL para iniciar el flujo de autenticación de OAuth
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "openid profile offline_access",
            "response_mode": "query",
            "state": "12345"
        }
        # Construye la URL de autorización completa
        auth_url = f"{self.authority_url}{self.authorize_endpoint}?{urllib.parse.urlencode(params)}"
        return auth_url

    def get_token_from_code(self, auth_code):
        # Intercambia el código por un token
        pass

    def validate_token(self, token):
        # Valida el token y obtiene información del usuario
        pass

    def login(self):
        # Método para iniciar el proceso de login
        auth_url = self.build_auth_url()
        return redirect(auth_url)

    def login_redirect(self):
        # Método que maneja la redirección después de la autenticación
        auth_code = request.args.get('code')
        token = self.get_token_from_code(auth_code)
        user_info = self.validate_token(token)
        if user_info:
            session['user_info'] = user_info
            return redirect(url_for('index'))  # Redirige a la página principal
        else:
            return "Error en la autenticación", 401

    def logout(self):
        # Método para cerrar la sesión del usuario
        session.pop('user_info', None)
        return redirect(url_for('index'))  # Redirige a la página de inicio de sesión o página principal
