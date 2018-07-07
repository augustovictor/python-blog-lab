from src import app
from flask import render_template, redirect, url_for, flash, session, abort
from .form import SetupForm, PostForm
from .models import Blog
from src.author.models import Author
from src import db
import bcrypt
from src.author.decorators import login_required, author_required

@app.route('/')
@app.route('/index')
def index():
    return 'Hey you!'

@app.route('/author')
def new_author():
    return render_template('blog/admin.html')

@app.route('/admin')
@author_required
def admin():
    if session.get('is_author'):
        return render_template('blog/admin.html')
    return abort(403)

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

@app.route('/posts', methods=['GET', 'POST'])
@author_required
def post():
    form = PostForm()
    return render_template('blog/post.html', form=form)

@app.route('/article')
def article():
    return render_template('blog/article.html')