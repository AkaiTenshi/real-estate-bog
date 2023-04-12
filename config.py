import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    KEYCLOAK_SERVER_URL= os.getenv('KEYCLOAK_SERVER_URL')
    KEYCLOAK_CLIENT_ID= os.getenv('KEYCLOAK_CLIENT_ID')
    KEYCLOAK_REALM_NAME= os.getenv('KEYCLOAK_REALM_NAME')
    KEYCLOAK_CLIENT_SECRET_KEY= os.getenv('KEYCLOAK_CLIENT_SECRET_KEY')
    KEYCLOAK_ADMIN_USERNAME= os.getenv('KEYCLOAK_ADMIN_USERNAME')
    KEYCLOAK_ADMIN_PASSWORD= os.getenv('KEYCLOAK_ADMIN_PASSWORD')