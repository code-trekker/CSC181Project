import datetime as datetime
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from wtforms.fields.html5 import DateField, DateTimeField

class LoginForm(FlaskForm):
    userid = StringField('Username', validators=[InputRequired(), Length(min=8, max=9, message="Invalid input")])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=12, message=None)])

class ViewLogin(FlaskForm):
    memberid = IntegerField('Student ID', validators=[InputRequired()])

class NewMember(FlaskForm):
    memberid = IntegerField('ID number', validators=[InputRequired()])
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


class NewBudget(FlaskForm):
    schoolyear = SelectField(u'School Year', choices=[('2015-2016','2015-2016'), ('2016-2017','2016-2017'), ('2017-2018','2017-2018'),
                                                      ('2018-2019','2018-2019'), ('2019-2020','2019-2020'), ('2020-2021','2020-2021'),
                                                      ('2021-2022', '2021-2022'), ('2022-2023','2022-2023'), ('2023-2024','2023-2024'),
                                                      ('2024-2025', '2024-2025'), ('2025-2026','2025-2026'), ('2026-2027','2026-2027'),
                                                      ('2027-2028', '2027-2028'), ('2028-2029','2028-2029'), ('2029-2030','2029-2030'),
                                                      ('2030-2031', '2030-2031'), ('2031-2032', '2031-2032'), ('2032-2033', '2032-2033'),
                                                      ('2033-2034', '2033-2034'), ('2034-2035', '2034-2035'), ('2035-2036', '2035-2036'),
                                                      ('2036-2037', '2036-2037'), ('2037-2038', '2037-2038'), ('2038-2039', '2038-2039'),
                                                      ('2039-2040', '2039-2040'), ('2040-2041', '2040-2041'), ('2041-2042', '2041-2042'),
                                                      ('2042-2043', '2042-2043'), ('2043-2044', '2043-2044'), ('2044-2045', '2044-2045')], validators=[InputRequired()])
    semester = SelectField(u'Semester', choices=[('FIRST', '1st'), ('SECOND', '2nd')], validators=[InputRequired()])
    budgetBal = DecimalField('Amount', validators=[InputRequired()], default=0)

class NewEvent(FlaskForm):
    eventid = IntegerField('Event ID', validators=[InputRequired()])
    eventName = StringField('Event Name', validators=[InputRequired(), Length(min=5,max=30, message='Invalid input')])
    eventDate = DateField('Event Date', format='%Y-%m-%d')
    allocation = DecimalField('Allocation', validators=[InputRequired()], default=0)

class UpEvent(FlaskForm):
    eventName = StringField('Event Name', validators=[InputRequired(), Length(min=5, max=30, message='Invalid input')])
    eventDate = DateField('Event Date', format='%Y-%m-%d')
    allocation = DecimalField('Allocation', validators=[InputRequired()], default=0)

class DelEvent(FlaskForm):
    eventid = StringField('Event ID', validators=[InputRequired(), Length(min=4,max=4, message='Invalid event code')])

class NewExpense(FlaskForm):
    expid = IntegerField('ID', validators=[InputRequired()])
    eid = StringField('Event Code', validators=[InputRequired(), Length(min=4, max=4, message='Invalid event code')])
    amount = DecimalField('Amount', validators=[InputRequired()], default=0)
    date = DateField('Date Spent', format='%Y-%m-%d')
    orNo = StringField('OR Number', validators=[InputRequired(), Length(max=30, message='OR Number too long')])
    name = StringField('Name', validators=[InputRequired(), Length(max=50, message='Too many characters')])

class UpExpense(FlaskForm):
    amount = DecimalField('Amount', validators=[InputRequired()], default=0)
    date = DateField('Date Spent', format='%Y-%m-%d')
    orNo = StringField('OR Number', validators=[InputRequired(), Length(max=30, message='OR Number too long')])
    name = StringField('Name', validators=[InputRequired(), Length(max=50, message='Too many characters')])

class DelExpense(FlaskForm):
    expid = IntegerField('ID', validators=[InputRequired(), Length(min=4, max=4, message='Invalid ID')])

class NewCollection(FlaskForm):
    #type = SelectField(u'Type', choices=[('assessment', 'Assessment'), ('tshirt', 'T-shirt'), ('lanyard', 'Lanyard'), ('others', 'Others')])
    colname = StringField('Collection Name', validators=[InputRequired(), Length(min=3, max=20, message="Input must be between 5-20 characters")])
    fee = DecimalField('Set Amount', validators=[InputRequired()])

class UpCollection(FlaskForm):
    colname = StringField('Collection Name', validators=[InputRequired(), Length(min=3, max=20, message="Input must be between 5-20 characters")])
    fee = DecimalField('Set Amount', validators=[InputRequired()], default=0)

class NewPayment(FlaskForm):
    memberid = IntegerField('Student ID', validators=[InputRequired()])
    datetime = DateField('Date Paid', format='%Y-%m-%d')

class NewAttendance(FlaskForm):
    memberid = IntegerField('Student ID', validators=[InputRequired()])
    attendtype = SelectField(u'Attendance Type', choices=[('IN', 'Sign In'), ('OUT', 'Sign Out')])