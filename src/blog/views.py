from src import app
from flask import render_template, redirect, url_for, flash
from .form import SetupForm
from .models import Blog
from src.author.models import Author
from src import db
import bcrypt

@app.route('/')
@app.route('/index')
def index():
    return 'Hey you!'

@app.route('/author')
def new_author():
    return render_template('blog/admin.html')

@app.route('/admin')
def admin():
    blogs = Blog.query.count()
    if blogs == 0:
        return redirect(url_for('setup'))
    return render_template('blog/admin.html')

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    error = None
    form = SetupForm()
    if form.validate_on_submit():
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(form.password.data, salt)
        author = Author(
            form.fullname.data,
            form.email.data,
            form.username.data,
            hash_password,
            True
        )

        db.session.add(author)
        db.session.flush() # mimic insertion to get row id
        
        if author.id:
            blog = Blog(form.name.data,author.id)
            db.session.add(blog)
            db.session.flush()
        else:
            db.session.rollback()
            error = 'Error creating user'
        
        if author.id and blog.id:
            db.session.commit()
            return render_template('blog/admin.html')
        else:
            db.session.rollback()
            error = 'Error creating blog'
        
        if error is None:
            flash('Blog created')
            return redirect(url_for('admin'))
        

    return render_template('blog/setup.html', form=form, error=error)