from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class SignupForm(FlaskForm):
    usuario = StringField('usuario')
    password = PasswordField('password')
    submit = SubmitField("Sign In")