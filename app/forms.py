from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *

class LoginForm(FlaskForm):
    userid = StringField('User ID', validators=[InputRequired(), Length(min=5, max=9, message="Invalid input")])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=12, message=None)])


class NewMember(FlaskForm):
    memberid = StringField('ID number', validators=[InputRequired(), Length(min=8, max=8, message="ID must be 8 characters long.")])
    fname = StringField('First Name', validators=[InputRequired(), Length(min=3, max=30, message="Must be at least 3 characters long")])
    mname = StringField('Middle Name', validators=[InputRequired(), Length(min=2, max=20, message="Must be at least 2 characters long")])
    lname = StringField('Last Name', validators=[InputRequired(), Length(min=2, max=20, message="Must be at least 2 characters long")])
    course = StringField('Course Name', validators=[InputRequired(), Length(min=10, max=30, message="Must be at least 10 characters long")])
    orgCode= SelectField(u'Organization', choices=[('SCS', 'School of Computer Studies'),
                                                   ('CBAA', 'College of Business Administration'),
                                                   ('CSM', 'College of Science and Mathematics'),
                                                   ('COET', 'College of Engineering Technology'),
                                                   ('CASS', 'College of Arts and Social Sciences'),
                                                   ('CON', 'College of Nursing'),
                                                   ('CED', 'College of Education')], validators=[InputRequired()])