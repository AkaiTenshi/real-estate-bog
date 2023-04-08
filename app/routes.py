from flask import render_template, request
from . import app

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # TODO: Handle login form submission
        pass
    return render_template('login.html')
