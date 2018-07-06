from flask_wtf import Form
from wtforms import validators, StringField
from src.author.form import RegisterForm

class SetupForm(RegisterForm):
    name = StringField('Blog name', [validators.DataRequired(), validators.Length(max=80)])
