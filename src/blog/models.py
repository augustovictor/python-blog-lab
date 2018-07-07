from src import db
from datetime import datetime

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    admin = db.Column(db.Integer, db.ForeignKey('author.id'))

    posts = db.relationship('Post', backref='blog', lazy='dynamic')

    def __init__(self, name, admin):
        self.name = name
        self.admin = admin
    
    def __repr__(self):
        return self.name

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    title = db.Column(db.String(255))
    body = db.Column(db.Text)
    slug = db.Column(db.String(255), unique=True)
    is_published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime)

    def __init__(self, blog, author, category, title, body, slug=None, is_published=False, created_at=None):
        self.blog_id = blog.id
        self.author_id = author.id
        self.category_id = category.id
        self.title = title
        self.body = body
        self.slug = slug
        self.is_published = is_published
        self.created_at = created_at if created_at else datetime.utcnow()

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return self.title