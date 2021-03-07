from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user
from company_blog.models import User

# Login
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

# Registration
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('UserName', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', 'Passwords must match!')])
    pass_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register!')

    # Make sure there isn't already an account that uses that same email
    def check_email(self, field):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Your email has been registered already!')

    # Make sure username is unique as well
    def check_username(self, field):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('That username has been registered already!')

# Updating user
class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('UserName', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    # Make sure there isn't already an account that uses that same email
    def check_email(self, field):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Your email has been registered already!')

    # Make sure username is unique as well
    def check_username(self, field):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('That username has been registered already!')
