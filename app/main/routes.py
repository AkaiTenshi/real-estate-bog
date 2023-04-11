from app.main import bp
from auth import KeycloakAuth
from flask import Flask

app = Flask(__name__)
auth = KeycloakAuth(app)

@bp.route('/')
@auth.protect('/')
def index():
    return 'This is The Main Blueprint'


@bp.route('/login')
def login():
    return 'This is the Login Page'