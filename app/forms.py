from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import  ValidationError, Length, DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from app.models import Class, Major


def get_major():
    return Major.query.all()


def get_major_label(theMajor):
    return theMajor.name

class ClassForm(FlaskForm):
    coursenum = StringField('Course Number',[Length(min=3, max=3)])
    title = StringField("Course Title", validators=[DataRequired()])
    major = QuerySelectField('Majors', query_factory=get_major, get_label=get_major_label, allow_blank=False)
    submit = SubmitField('Post')
