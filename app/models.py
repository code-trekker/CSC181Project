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
    course = db.Column(db.String(30), nullable=False)
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