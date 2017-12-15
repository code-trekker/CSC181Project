from controller import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects import mysql

Integer = mysql.INTEGER

class User(UserMixin, db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    userid = db.Column(db.String(20), unique=True, nullable=False)
    password =db.Column(db.String(100), nullable=False)
    orgCode=db.Column(db.String(5), nullable=False)

    def __init__(self, userid, password, orgCode):
        self.userid = userid
        self.password = password
        self.orgCode= orgCode

    def __repr__(self):
        return '<User %r>' % self.userid

    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.id)

class Themes(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True, autoincrement=True)
    theme = db.Column(db.String(32), nullable=False)
    def __init__(self, id, theme):
        self.id=id
        self.theme=theme

    def __repr__(self):
        return '<Themes %r>' % self.id


class Member(db.Model):
    memberid = db.Column(db.Integer(), primary_key=True, unique=True, autoincrement=False)
    fname = db.Column(db.String(30), nullable=False)
    mname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    course = db.Column(db.String(50), nullable=True)
    orgCode = db.Column(db.String(4), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    payment = db.relationship('Payments', backref='member', lazy=True)
    attends = db.relationship('Attendance', backref='member', lazy=True)
    themeid = db.Column(db.Integer(), db.ForeignKey('themes.id'), default=0)

    def __init__(self, memberid, fname, mname, lname, course, orgCode, status, themeid):
        self.memberid=memberid
        self.fname=fname
        self.mname=mname
        self.lname=lname
        self.course=course
        self.status=status
        self.orgCode=orgCode
        self.themeid=themeid

    def __repr__(self):
        return '<Member %r>' % self.fname

class Organization(db.Model):
    orgCode = db.Column(db.String(10), primary_key=True, autoincrement=False)
    orgName = db.Column(db.String(70), nullable=False, unique=True)
    description = db.Column(db.String(1200), nullable=False)
    budgets = db.relationship('Budget', backref='organization', lazy=True)
    events = db.relationship('Event', backref='organization', lazy=True)
    exp = db.relationship('Expenses', backref='organization', lazy=True)
    collect = db.relationship('Collection', backref='organization', lazy=True)
    payrec = db.relationship('Payments', backref='organization', lazy=True)
    logs = db.relationship('Logs', backref='organization', lazy=True)

    def __init__(self, orgCode, orgName, description):
        self.orgCode=orgCode
        self.orgName=orgName
        self.description=description

    def __repr__(self):
        return '<Organization %r>' %self.orgCode

class Collection(db.Model):
    colid = db.Column(db.Integer(), primary_key=True)
    colname = db.Column(db.String(35), nullable=False)
    fee = db.Column(db.DECIMAL(10, 2), nullable=False)
    amountcollected = db.Column(db.DECIMAL(10,2), nullable=False)
    Collection_orgCode=db.Column(db.String(10), db.ForeignKey('organization.orgCode'), nullable=False)
    schoolyear = db.Column(db.CHAR(4), nullable=False)
    pays = db.relationship('Payments', backref='collection', lazy=True)

    def __init__(self, colname, fee, amountcollected, Collection_orgCode, schoolyear):
        self.colname=colname
        self.fee=fee
        self.amountcollected = amountcollected
        self.Collection_orgCode=Collection_orgCode
        self.schoolyear=schoolyear

    def __repr__(self):
        return "%s" % (self.colname)

class Payments(db.Model):
    pid = db.Column(db.Integer(), primary_key=True)
    Payments_colid = db.Column(Integer(11), db.ForeignKey('collection.colid'), nullable=False)
    Payments_memberid = db.Column(Integer(11), db.ForeignKey('member.memberid'), nullable=False)
    datepaid = db.Column(db.CHAR(10), nullable=False)
    Payments_orgCode = db.Column(db.String(10), db.ForeignKey('organization.orgCode'), nullable=False)

    def __init__(self, Payments_colid, Payments_memberid, datepaid, Payments_orgCode):
        self.Payments_colid = Payments_colid
        self.Payments_memberid=Payments_memberid
        self.datepaid=datepaid
        self.Payments_orgCode=Payments_orgCode

    def __repr__(self):
        return '<Payments %r>' % self.Payments_orgCode

class Budget(db.Model):
    budgetid = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    schoolyear = db.Column(db.String(20), unique=False, nullable=False)
    semester = db.Column(db.String(8), unique=False, nullable=False)
    budgetBal = db.Column(db.DECIMAL(10,2), unique=False, nullable=False)
    Budget_orgCode = db.Column(db.String(10), db.ForeignKey('organization.orgCode'), nullable=False)

    def __init__(self, schoolyear, semester, budgetBal, Budget_orgCode):
        self.schoolyear=schoolyear
        self.semester=semester
        self.budgetBal=budgetBal
        self.Budget_orgCode=Budget_orgCode

    def __repr__(self):
        return '<Budget %r>' % self.Organization_orgCode

class Event(db.Model):
    eventid = db.Column(db.Integer(), primary_key=True)
    eventName = db.Column(db.String(30), unique=True, nullable=False)
    eventDate = db.Column(db.CHAR(10), nullable=False)
    allocation = db.Column(db.DECIMAL(10,2), nullable=False)
    Event_orgCode = db.Column(db.String(10), db.ForeignKey('organization.orgCode'), nullable=False)
    schoolyear = db.Column(db.CHAR(4), nullable=False)
    expense = db.relationship('Expenses',cascade='all,delete-orphan', backref=db.backref('expenses', cascade="all"), lazy=True, single_parent=True)
    attendance = db.relationship('Attendance', backref='event', lazy=True)

    def __init__(self, eventName, eventDate, allocation, Event_orgCode, schoolyear):
        self.eventName = eventName
        self.eventDate = eventDate
        self.allocation = allocation
        self.Event_orgCode = Event_orgCode
        self.schoolyear=schoolyear

    def __repr__(self):
        return "%s" % (self.eventName)

class Expenses(db.Model):
    expid = db.Column(db.Integer(), primary_key=True)
    Expenses_eventid = db.Column(db.Integer(), db.ForeignKey('event.eventid'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.DECIMAL(10,2), nullable=False)
    date = db.Column(db.CHAR(10), nullable=False)
    orNo = db.Column(db.String(30), nullable=False)
    Expenses_orgCode = db.Column(db.String(10), db.ForeignKey('organization.orgCode'), nullable=False)

    def __init__(self, amount, date, orNo, name, Expenses_eventid, Expenses_orgCode ):
        self.amount = amount
        self.date = date
        self.orNo = orNo
        self.name = name
        self.Expenses_eventid = Expenses_eventid
        self.Expenses_orgCode = Expenses_orgCode

    def __repr__(self):
        return '<Expenses %r>' % self.Expenses_orgCode

class Attendance(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    memberid = db.Column(Integer(8), db.ForeignKey('member.memberid'), nullable=False, unique=False)
    eventid = db.Column(db.Integer(), db.ForeignKey('event.eventid'), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    signin = db.Column(db.CHAR(5), nullable=True)
    signout = db.Column(db.CHAR(5), nullable=True)

    def __init__(self, memberid, eventid, date, signin, signout):
        self.memberid=memberid
        self.eventid=eventid
        self.date=date
        self.signin=signin
        self.signout=signout

    def __repr__(self):
        return '<Attendance %r>' % self.date


class Logs(db.Model):
    i = db.Column(db.Integer, primary_key=True)
    idno = db.Column(db.CHAR(8), nullable=False)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    dnt = db.Column(db.String(30), nullable=False)
    orgCode = db.Column(db.String(4), db.ForeignKey('organization.orgCode'), nullable=False, unique=False)

    def __init__(self, idno, fname, lname, dnt, orgCode):
        self.idno = idno
        self.fname = fname
        self.lname = lname
        self.dnt = dnt
        self.orgCode=orgCode

class Courses(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    coursename= db.Column(db.String(40), nullable=True)

    def __init__(self, coursename):
        self.coursename = coursename

    def __repr__(self):
        return "%s" % (self.coursename)


