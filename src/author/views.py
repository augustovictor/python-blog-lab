from src import app
from flask import render_template, redirect, url_for, session, request
from .form import RegisterForm, LoginForm
from .models import Author
from .decorators import login_required
import bcrypt

@app.route('/logout')
def logout():
    session.pop('username')
    session.pop('is_author')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None

    if request.method == 'GET' and request.args.get('next'):
        session['next'] = request.args.get('next', None)

    if form.validate_on_submit():
        author = Author.query.filter_by(username=form.username.data).first()

        if author and bcrypt.hashpw(form.password.data, author.password) == author.password:
            session['username'] = form.username.data
            session['is_author'] = author.is_author
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