from flask_wtf import Form
from wtforms import validators, StringField, PasswordField
from wtforms.fields.html5 import EmailField
    
class RegisterForm(Form):
    fullname = StringField('Name', [validators.Required()])
    email = EmailField('Email', [validators.Required()])
    username = StringField('Username', [
        validators.Required(),
        validators.Length(min=4, max=25)
    ])
    password = PasswordField('New password', [
        validators.Required(),
        validators.Length(min=3,max=80),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Repeat password')