from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired,Length, Email, EqualTo,ValidationError
from blog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already taken!')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    # password = PasswordField('Password', validators=[DataRequired()])
    # confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    picture = FileField('update profile picture',validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update profile')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is already taken!')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is already taken!')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    picture = FileField('add blog picture',validators=[FileAllowed(['jpg','png'])])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')