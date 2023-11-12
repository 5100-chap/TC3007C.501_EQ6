from flask import session, redirect, url_for, request, jsonify
import requests
import urllib.parse
import jwt
import os
import time
from config import varConfig

class AuthManager:
    def __init__(self, url, db_manager):
        # Configuración de Azure AD B2C
        self.tenant_id = varConfig.TENANT_ID
        self.client_id = varConfig.CLIENT_ID
        self.client_secret = varConfig.CLIENT_SECRET
        self.scope = "https://graph.microsoft.com/.default"
        self.grant_type = "client_credentials"
        self.token_url = varConfig.token_endpoint_signin # Asegúrate de que esta es la URL correcta para obtener el token
        self.redirect_uri = url + "/login-redirect"  # Asegúrate de cambiar esto a tu URI de redirección registrada
        self.authority_url = varConfig.authorize_url_signin
        self.response_type = 'code'  # Tipo de respuesta esperada, en este caso un código de autorización
        self.db_manager = db_manager

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
        separator = '&' if '?' in self.authority_url else '?'
        auth_url = f"{self.authority_url}{separator}{urllib.parse.urlencode(params)}"
        return jsonify({'state': state, 'authUrl': auth_url})

    def get_token_from_code(self, auth_code):
        token_params = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': auth_code,
            'redirect_uri': self.redirect_uri
        }

        response = requests.post(self.token_url, data=token_params)

        if response.status_code != 200:
            # Manejo del error
            raise Exception(f"Error en la solicitud del token: {response.status_code}, {response.text}")

        return response.json()


    def validate_token(self, token):
        try:
            # Decodifica el token. En producción, deberías verificar la firma aquí.
            # Necesitarías la clave pública de Azure AD B2C para hacer esto.
            decoded_token = jwt.decode(token, options={"verify_signature": False})

            # Valida afirmaciones importantes como issuer (iss), audience (aud), y expiration (exp)
            issuer = f"https://facenlearn2.b2clogin.com/{self.tenant_id}/v2.0/"
            if decoded_token['iss'] != issuer:
                raise ValueError("Issuer Mismatch")
            if decoded_token['aud'] != self.client_id:
                raise ValueError("Audience Mismatch")
            if decoded_token['exp'] < int(time.time()):
                raise ValueError("Token Expired")
            email = decoded_token['emails'][0]
            user_role = self.db_manager.get_user_role(email)
            decoded_token['user_role'] = user_role

            return decoded_token
        except jwt.PyJWTError as e:
            # Maneja la excepción si la validación del token falla
            print(f"Error al validar el token: {e}")
            return None


    def login(self):
        # Método para iniciar el proceso de login
        auth_url = self.build_auth_url()
        return auth_url
    
    def login_redirect(self):
        # Método que maneja la redirección después de la autenticación
        auth_code = request.args.get('code')
        state = request.args.get('state')
        # Verifica que el estado coincida con el enviado en la solicitud original
        s = session.get('state')
        if state != session.get('state'):
            return "Error de estado inválido", 400
        token_response = self.get_token_from_code(auth_code)
        token = token_response.get('id_token')
        user_info = self.validate_token(token)
        if user_info:
            encoded_jwt = jwt.encode(user_info, varConfig.FLASK_SECRET_KEY, algorithm='HS256')

            return jsonify({'jwt': encoded_jwt})
        else:
            return "Error en la autenticación", 401
        
    def logout(self):
        # Método para cerrar la sesión del usuario
        session.pop('user_info', None)
        session.pop('state', None)
        return redirect(url_for('index'))  # Redirige a la página de inicio de sesión o página principal
