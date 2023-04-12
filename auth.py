from flask import session, request, redirect, url_for
from keycloak import KeycloakOpenID, KeycloakAdmin
from keycloak.exceptions import KeycloakAuthenticationError
from config import Config as config_class
from functools import wraps

class KeycloakAuth:
    def __init__(self, app):
        self.app = app
        app.config.from_object(config_class)
        self.keycloak_openid = KeycloakOpenID(
            server_url=config_class.KEYCLOAK_SERVER_URL,
            client_id=config_class.KEYCLOAK_CLIENT_ID,
            realm_name=config_class.KEYCLOAK_REALM_NAME,
            client_secret_key=config_class.KEYCLOAK_CLIENT_SECRET_KEY)
        self.keycloak_admin = KeycloakAdmin(
            server_url=config_class.KEYCLOAK_SERVER_URL,
            username=config_class.KEYCLOAK_ADMIN_USERNAME,
            password=config_class.KEYCLOAK_ADMIN_PASSWORD,
            realm_name=config_class.KEYCLOAK_REALM_NAME,
            client_secret_key=config_class.KEYCLOAK_CLIENT_SECRET_KEY)

    def protect(self, directory):
        def keycloak_protect(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                if directory in request.path:
                    if 'access_token' not in session:
                        return redirect(url_for('auth.login'))
                    #try:
                        #self.keycloak_openid.userinfo(session['access_token'])
                    #except KeycloakAuthenticationError:
                        #return redirect(url_for('auth.login'))
                return f(*args, **kwargs)
            return decorated
        return keycloak_protect

    def login(self, username, password):
        try:
            token = self.keycloak_openid.token(username, password)
            session['access_token'] = token['access_token']
            session['refresh_token'] = token['refresh_token']
            session['id_token'] = token['id_token']
            return True
        except KeycloakAuthenticationError:
            return False

    def logout(self):
        session.clear()

    def register(self, password, email):
        try:
            self.create_user(email, password)
            return True
        except KeycloakAuthenticationError:
            return False
        
    def get_token(self, username, password):
            return self.keycloak_openid.token(username, password)
        
    def get_userinfo(self, token):
            return self.keycloak_openid.userinfo(token['access_token'])
        
    def create_user(self, email, password):
        # Create user in Keycloak
        user = {
            'email': email,
            'enabled': True,
            'username': email,
            'credentials': [{'type': 'password', 'value': password, 'temporary': False}]
        }
        self.keycloak_admin.create_user(user)