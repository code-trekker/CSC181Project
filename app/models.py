from controller import *
from sqlalchemy.orm import relationship, backref

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

class Member(db.Model):
    memberid = db.Column(db.Integer(), primary_key=True, unique=True, autoincrement=False)
    fname = db.Column(db.String(30), nullable=False)
    mname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    course = db.Column(db.String(50), nullable=False)
    orgCode = db.Column(db.String(4), nullable=False)

    def __init__(self, memberid, fname, mname, lname, course, orgCode):
        self.memberid=memberid
        self.fname=fname
        self.mname=mname
        self.lname=lname
        self.course=course
        self.orgCode=orgCode

    def __repr__(self):
        return '<Member %r>' % self.fname

class Organization(db.Model):
    orgCode = db.Column(db.String(10), primary_key=True, autoincrement=False)
    orgName = db.Column(db.String(70), nullable=False, unique=True)
    budgets = db.relationship('Budget', backref='organization', lazy=True)
    events = db.relationship('Event', backref='organization', lazy=True)
    exp = db.relationship('Expenses', backref='organization', lazy=True)

    def __init__(self, orgCode, orgName):
        self.orgCode=orgCode
        self.orgName=orgName

    def __repr__(self):
        return '<Organization %r>' %self.orgCode

class Budget(db.Model):
    budgetid = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    schoolyear = db.Column(db.String(20), unique=False, nullable=False)
    semester = db.Column(db.String(8), unique=False, nullable=False)
    budgetBal = db.Column(db.DECIMAL(10,2), unique=False, nullable=False)
    Organization_orgCode = db.Column(db.String(10), db.ForeignKey('organization.orgCode'), nullable=False)

    def __init__(self, schoolyear, semester, budgetBal, Organization_orgCode):
        self.schoolyear=schoolyear
        self.semester=semester
        self.budgetBal=budgetBal
        self.Organization_orgCode=Organization_orgCode

    def __repr__(self):
        return '<Budget %r>' % self.Organization_orgCode

class Event(db.Model):
    eventid = db.Column(db.String(4), primary_key=True, autoincrement=False)
    eventName = db.Column(db.String(30), unique=True, nullable=False)
    eventDate = db.Column(db.String(11), nullable=False)
    allocation = db.Column(db.DECIMAL(10,2), nullable=False)
    Event_orgCode = db.Column(db.String(10), db.ForeignKey('organization.orgCode'), nullable=False)
    expense = db.relationship('Expenses', backref='expenses', lazy=True)

    def __init__(self, eventid, eventName, eventDate, allocation, Event_orgCode):
        self.eventid = eventid
        self.eventName = eventName
        self.eventDate = eventDate
        self.allocation = allocation
        self.Event_orgCode = Event_orgCode

    def __repr__(self):
        return '<Event %r>' % self.Event_orgCode

class Expenses(db.Model):
    expid = db.Column(db.Integer(), primary_key=True)
    Expenses_eventid = db.Column(db.String(4), db.ForeignKey('event.eventid'), nullable=False)
    amount = db.Column(db.DECIMAL(10,2), nullable=False)
    date = db.Column(db.String(11), nullable=False)
    orNo = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(50), nullable=False)
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
