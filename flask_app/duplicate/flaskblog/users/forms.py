from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Email,EqualTo,ValidationError,Length
from flaskblog.models import User
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=1,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=10)])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already taken! Pick another!')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email already registered! Login to continue!')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember')
    submit = SubmitField('Login')

class AccountForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=1,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    image_file = FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_username(self,username):
        if(username.data!=current_user.username):
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('Username already taken! Pick another!')

    def validate_email(self,email):
        if(email.data!=current_user.email):
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('Email already registered! Login to continue!')

class RequestResetForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField('Get Link')
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Email not found!')

class PasswordResetForm(FlaskForm):
    password = PasswordField('Password',validators=[DataRequired(),Length(min=10)])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Reset')
