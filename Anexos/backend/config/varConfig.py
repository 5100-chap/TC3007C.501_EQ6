from dotenv import load_dotenv
import os
import re

# Carga las variables de entorno desde el archivo .env en el mismo directorio
load_dotenv()

# Variables de configuración de Microsoft Azure AD b2c
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Configuración de Azure SQL
AZURE_SQL_CONNECTION_STRING = os.getenv("AZURE_SQL_CONNECTION_STRING")
AZURE_SQL_CONNECTION_STRING_TCP= os.getenv("AZURE_SQL_CONNECTION_STRING_TCP")



connection_string = AZURE_SQL_CONNECTION_STRING_TCP

DBserver = re.search(r'tcp:(.*?),', connection_string).group(1)
DBuser = re.search(r'User ID=(.*?);', connection_string).group(1)
DBpassword = re.search(r'Password=(.*?);', connection_string).group(1)
DBname = re.search(r'Initial Catalog=(.*?);', connection_string).group(1)
DBport = re.search(r',(\d+);', connection_string).group(1)

# Configuración de Azure Blob Storage
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_STORAGE_CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER_NAME")

# Llave secreta para flask
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

# Base URL para Azure AD b2c
BASE_URL = "https://facenlearn2.b2clogin.com/facenlearn2.onmicrosoft.com/"

# Función para construir URLs específicas de la política
def build_policy_url(policy_name, endpoint_type):
    if endpoint_type == "token":
        endpoint = "oauth2/v2.0/token"
    elif endpoint_type == "authorize":
        endpoint = "oauth2/v2.0/authorize"
    elif endpoint_type == "logout":
        endpoint = "oauth2/v2.0/logout"
    else:
        raise ValueError("Invalid endpoint type")

    return f"{BASE_URL}{policy_name}/{endpoint}"

# Políticas de User Flows
policies = [
    "b2c_1_face_n_lean_signinonly",
    "b2c_1_face_n_learn_password_reset",
    "b2c_1_face_n_learn_registration",
    "b2c_1_face_n_learn_signup_signin"
]

# Endpoints
endpoints = ["token", "authorize", "logout"]

# Diccionario para almacenar las URLs construidas
policy_urls = {}

# Construcción de URLs
for policy in policies:
    for endpoint in endpoints:
        key = f"{policy}_{endpoint}"
        policy_urls[key] = build_policy_url(policy, endpoint)

# Extraer las URLs para la política de inicio de sesion
token_endpoint_signin = policy_urls["b2c_1_face_n_lean_signinonly_token"]
authorize_url_signin = policy_urls["b2c_1_face_n_lean_signinonly_authorize"]
logout_url_signin = policy_urls["b2c_1_face_n_lean_signinonly_logout"]

# Extraer las URLs para la política de reseteo de contraseña
token_endpoint_password_reset = policy_urls["b2c_1_face_n_learn_password_reset_token"]
authorize_url_password_reset = policy_urls["b2c_1_face_n_learn_password_reset_authorize"]
logout_url_password_reset = policy_urls["b2c_1_face_n_learn_password_reset_logout"]

# Extraer las URLs para la política de registro
token_endpoint_registration = policy_urls["b2c_1_face_n_learn_registration_token"]
authorize_url_registration = policy_urls["b2c_1_face_n_learn_registration_authorize"]
logout_url_registration = policy_urls["b2c_1_face_n_learn_registration_logout"]

# Extraer las URLs para la política de registro e inicio de sesión
token_endpoint_signup_signin = policy_urls["b2c_1_face_n_learn_signup_signin_token"]
authorize_url_signup_signin = policy_urls["b2c_1_face_n_learn_signup_signin_authorize"]
logout_url_signup_signin = policy_urls["b2c_1_face_n_learn_signup_signin_logout"]
