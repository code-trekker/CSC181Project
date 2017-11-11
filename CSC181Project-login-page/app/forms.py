from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *

class LoginForm(FlaskForm):
    userid = StringField('User ID', validators=[InputRequired(), Length(min=5, max=20)])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember Me')

class NewMember(FlaskForm):
    id = StringField('id', validators=[InputRequired(), Length(min=9, max=9)])
    fname = StringField('fname', validators=[InputRequired(), Length(min=3, max=30)])
    mname = StringField('mname', validators=[InputRequired(), Length(min=2, max=20)])
    lname = StringField('mname', validators=[InputRequired(), Length(min=2, max=20)])
    course = StringField('course', validators=[InputRequired(), Length(min=10, max=30)])
    orgCode= SelectField(u'Organization', choices=[('SCS', 'School of Computer Studies'),
                                                   ('CBAA', 'College of Business Administration'),
                                                   ('CSM', 'College of Science and Mathematics'),
                                                   ('COET', 'College of Engineering Technology'),
                                                   ('CASS', 'College of Arts and Social Sciences'),
                                                   ('CON', 'College of Nursing'),
                                                   ('CED', 'College of Education')])