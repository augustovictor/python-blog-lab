from flask_wtf import Form
from wtforms import validators, StringField, PasswordField
from wtforms.fields.html5 import EmailField
    
class RegisterForm(Form):
    fullname = StringField('Name', [validators.DataRequired()])
    email = EmailField('Email', [validators.DataRequired()])
    username = StringField('Username', [
        validators.DataRequired(),
        validators.Length(min=4, max=25)
    ])
    password = PasswordField('New password', [
        validators.DataRequired(),
        validators.Length(min=3,max=80),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Repeat password')