from flask_wtf import Form
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import validators, StringField, TextAreaField
from src.author.form import RegisterForm
from src.blog.models import Category

class SetupForm(RegisterForm):
    name = StringField('Blog name', [validators.DataRequired(), validators.Length(max=80)])

def categories():
    return Category.query

class PostForm(Form):
    title = StringField('Title', [validators.DataRequired(), validators.Length(max=80)])
    body = TextAreaField('Body', [validators.DataRequired()])
    category = QuerySelectField('Category', query_factory=categories, allow_blank=True)
    new_category = StringField('New category')
