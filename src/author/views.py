from src import app
from flask import render_template, redirect, url_for, session, request
from .form import RegisterForm, LoginForm
from .models import Author
from .decorators import login_required
import bcrypt

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None

    if request.method == 'GET' and request.args.get('next'):
        session['next'] = request.args.get('next', None)

    if form.validate_on_submit():
        authors = Author.query.filter_by(username=form.username.data).limit(1)

        if authors.count() and bcrypt.hashpw(form.password.data, authors[0].password) == authors[0].password:
            session['username'] = form.username.data
            if 'next' in session:
                next = session.get('next')
                session.pop('next')
                return redirect(next)
            return 'Logged in without next in session'
        else:
            error = 'Invalid credentials'
    return render_template('author/login.html', form=form, error=error)

@app.route('/signup', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        return redirect(url_for('success'))
    return render_template('author/register.html', form=form)

@app.route('/success')
def success():
    return 'Registered successfully!'

@app.route('/login-success')
@login_required
def login_success():
    return 'Logged in successfully!'