from flask import session, request, redirect, url_for
from keycloak import KeycloakOpenID
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
            client_secret_key=config_class.KEYCLOAK_CLIENT_SECRET_KEY,
        )

    def protect(self, directory):
        def keycloak_protect(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                if directory in request.path:
                    if 'access_token' not in session:
                        return redirect(url_for('main.login'))
                    try:
                        self.keycloak_openid.userinfo(session['access_token'])
                    except KeycloakAuthenticationError:
                        return redirect(url_for('main.login'))
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

    def register(self, username, password, email):
        try:
            self.keycloak_openid.create_user(
                {'username': username, 'email': email, 'enabled': True},
                password,
            )
            return True
        except KeycloakAuthenticationError:
            return False
