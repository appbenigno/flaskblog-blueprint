from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    username = StringField(label='Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = EmailField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        label='Confirm Password', validators=[DataRequired(), EqualTo(fieldname='password')])
    submit = SubmitField(label='Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember = BooleanField(label='Remember Me')
    submit = SubmitField(label='Login')


class UpdateAccountForm(FlaskForm):
    username = StringField(label='Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = EmailField(label='Email', validators=[DataRequired(), Email()])
    picture = FileField(label='Update Profile Picture', validators=[
                        FileAllowed(upload_set=['jpg', 'png'])])
    submit = SubmitField(label='Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            theUser = User.query.filter_by(username=username.data).first()
            if theUser:
                raise ValidationError(
                    'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            theEmail = User.query.filter_by(email=email.data).first()
            if theEmail:
                raise ValidationError(
                    'That email is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired(), Email()])
    submit = SubmitField(label='Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                'There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(label='Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        label='Confirm Password', validators=[DataRequired(), EqualTo(fieldname='password')])
    submit = SubmitField(label='Reset Password')
