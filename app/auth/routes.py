from flask import render_template, redirect, url_for, Flask, flash
from flask import session, request
from app.auth import bp
from auth import KeycloakAuth
from app.auth.forms import LoginForm, RegistrationForm

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
        if form.validate_on_submit():
            username = request.form.get('username')
            password = request.form.get('password')
            email = request.form.get('email')
            if auth.username_exists(username):
                flash('Username already exists')
                return redirect(url_for('auth.login'))
            if auth.email_exists(email):
                flash('Email already exists')
                return redirect(url_for('auth.login'))
            if auth.register(username, password, email):
                flash('Registration successful. Verify your email and login', 'success')
                return redirect(url_for('auth.login'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('auth/register.html', form=form)

@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    auth.logout()
    return redirect(url_for('auth.login'))
