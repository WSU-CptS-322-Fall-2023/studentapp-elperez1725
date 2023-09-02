from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import  ValidationError, Length, DataRequired, EqualTo
from wtforms_sqlalchemy.fields import QuerySelectField
from app.models import Class, Major, Student


def get_major():
    return Major.query.all()


def get_major_label(theMajor):
    return theMajor.name

class ClassForm(FlaskForm):
    coursenum = StringField('Course Number',[Length(min=3, max=3)])
    title = StringField("Course Title", validators=[DataRequired()])
    major = QuerySelectField('Majors', query_factory=get_major, get_label=get_major_label, allow_blank=False)
    submit = SubmitField('Post')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    address = TextAreaField('Address', [Length(min=0, max=100)])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Register")

    def validate_username(self, username):
        student = Student.query.filter_by(username=username.data).first()
        if student is not None:
            raise ValidationError('The username already exists! Plase use a different username.')
        
    def validate_eamil(self, email):
        student = Student.query.filter_by(email=email.data).first()
        if student is not None:
            raise ValidationError('The email already exists! Plase use a different email address.')
        
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me', validators=[DataRequired()])
    submit = SubmitField("Sign In")