from flask import session, redirect, url_for, request
import requests
import urllib.parse
import jwt
import os
from config import varConfig

class AuthManager:
    def __init__(self, url):
        # Configuración de Azure AD B2C
        self.tenant_id = varConfig.TENANT_ID
        self.client_id = varConfig.CLIENT_ID
        self.client_secret = varConfig.CLIENT_SECRET
        self.scope = "https://graph.microsoft.com/.default"
        self.grant_type = "client_credentials"
        self.token_url = varConfig.TOKEN_ENDPOINT  # Asegúrate de que esta es la URL correcta para obtener el token
        self.redirect_uri = url + "/login-redirect"  # Asegúrate de cambiar esto a tu URI de redirección registrada
        self.authority_url = varConfig.AUTHORITY_URL
        self.response_type = 'code'  # Tipo de respuesta esperada, en este caso un código de autorización

    def build_auth_url(self):
        # Construye la URL para iniciar el flujo de autenticación de OAuth
        state = os.urandom(16).hex()  # Genera un estado aleatorio
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "openid profile offline_access",
            "response_mode": "query",
            "state": state
        }
        # Guarda el estado en la sesión para su posterior verificación
        session['state'] = state
        # Construye la URL de autorización completa
        auth_url = f"{self.authority_url}?{urllib.parse.urlencode(params)}"
        return auth_url

    def get_token_from_code(self, auth_code):
        # Parámetros para la solicitud de token
        token_params = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'scope': self.scope,
            'code': auth_code,
            'redirect_uri': self.redirect_uri,
            'client_secret': self.client_secret
        }

        # Realiza la solicitud POST para obtener el token
        response = requests.post(self.token_url, data=token_params)
        response.raise_for_status()  # Lanza una excepción si la solicitud no fue exitosa

        # Decodifica la respuesta JSON para obtener el token
        token_response = response.json()
        return token_response

    def validate_token(self, token):
        # Valida el token y obtiene información del usuario
        # Aquí deberías implementar la lógica de validación del token, como verificar la firma y las afirmaciones
        try:
            # Decodifica el token sin verificar la firma (esto debería hacerse con la clave pública de Azure AD B2C)
            decoded_token = jwt.decode(token, options={"verify_signature": False})
            # Aquí deberías verificar la firma y las afirmaciones del token
            return decoded_token
        except jwt.PyJWTError as e:
            # Maneja la excepción si la validación del token falla
            print(f"Error al validar el token: {e}")
            return None

    def login(self):
        # Método para iniciar el proceso de login
        auth_url = self.build_auth_url()
        return redirect(auth_url)

    def login_redirect(self):
        # Método que maneja la redirección después de la autenticación
        auth_code = request.args.get('code')
        state = request.args.get('state')
        # Verifica que el estado coincida con el enviado en la solicitud original
        if state != session.get('state'):
            return "Error de estado inválido", 400
        token_response = self.get_token_from_code(auth_code)
        token = token_response.get('access_token')
        user_info = self.validate_token(token)
        if user_info:
            session['user_info'] = user_info
            return redirect(url_for('index'))  # Redirige a la página principal
        else:
            return "Error en la autenticación", 401
        
    def logout(self):
        # Método para cerrar la sesión del usuario
        session.pop('user_info', None)
        session.pop('state', None)
        return redirect(url_for('index'))  # Redirige a la página de inicio de sesión o página principal
