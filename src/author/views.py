from src import app
from flask import render_template, redirect, url_for, session
from .form import RegisterForm, LoginForm
from .models import Author

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None

    if form.validate_on_submit():
        author = Author.query.filter_by(username=form.username.data, password=form.password.data).limit(1)
        if author.count():
            session['username'] = form.username.data
            return redirect(url_for('login_success'))
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
def login_success():
    return 'Logged in successfully!'