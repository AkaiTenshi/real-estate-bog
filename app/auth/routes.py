from flask import render_template, redirect, url_for, Flask, flash
from flask import session, request
from app.auth import bp
from auth import KeycloakAuth
from .forms import LoginForm, RegistrationForm

app = Flask(__name__)
auth = KeycloakAuth(app)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        redirect_url = request.form.get('redirect_url')
        if form.validate_on_submit():
            if auth.login(username, password):
                session['access_token'] = auth.get_token(username, password)
                return redirect(redirect_url or url_for('main.index'))
            else:
                flash('Invalid username or password', 'danger')
    return render_template('auth/login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        if form.validate_on_submit():
            if auth.register(username, password, email):
                return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)

@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    auth.logout()
    return redirect(url_for('auth.login'))
