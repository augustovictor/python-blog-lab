from src import app
from flask import render_template, redirect, url_for, flash, session, abort
from .form import SetupForm, PostForm
from .models import Blog, Category, Post
from src.author.models import Author
from src import db
import bcrypt
from slugify import slugify
from src.author.decorators import author_required

POSTS_PER_PAGE = 3

@app.route('/author')
def new_author():
    return render_template('blog/admin.html')

@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>')
def index(page=1):
    # True returns 404 for not existent pages
    # False returns empty list
    posts = Post.query.order_by(Post.created_at.desc()).paginate(page, POSTS_PER_PAGE, False)
    return render_template('blog/admin.html', posts=posts)

@app.route('/admin')
@author_required
def admin():
    if session.get('is_author'):
        posts = Post.query.order_by(Post.created_at.desc())
        return render_template('blog/admin.html', posts=posts)
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
    if form.validate_on_submit():
        category = None

        if form.new_category.data:
            new_category = Category(form.new_category.data)
            db.session.add(new_category)
            db.session.flush()
            category = new_category
        elif form.category.data:
            category_id = form.category.get_pk(form.category.data)
            category = Category.query.filter_by(id=category_id).first()

        blog = Blog.query.first()
        author = Author.query.filter_by(username=session['username']).first()
        title = form.title.data
        body = form.body.data
        slug = slugify(title)

        post = Post(blog, author, category, title, body, slug)

        db.session.add(post)
        db.session.commit()
        return redirect((url_for('admin')))
    return render_template('blog/post.html', form=form)

@app.route('/article')
def article():
    return render_template('blog/article.html')

@app.route('/article/<slug>')
def get_article(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template('blog/article.html', post=post)

@app.route('/delete/<int:post_id>')
@author_required
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.is_published = False
    db.session.commit()
    return redirect('admin')

@app.route('/edit/<int:post_id>')
@author_required
def edit_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    form = PostForm(obj=post)
    return render_template('blog/post.html', form=form, post=post, action='edit')
