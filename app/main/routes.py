from app.main import bp
from auth import KeycloakAuth
from flask import Flask, render_template, session

app = Flask(__name__)
auth = KeycloakAuth(app)

@bp.route('/')
@auth.protect('/')
def index():
    current_user = auth.get_userinfo(session.get('access_token'))
    return render_template('main/index.html', current_user=current_user)
