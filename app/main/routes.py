from app.main import bp
from auth import KeycloakAuth
from flask import Flask, render_template, session

app = Flask(__name__)
auth = KeycloakAuth(app)

@bp.route('/')
def index():
    return render_template('main/index.html')
