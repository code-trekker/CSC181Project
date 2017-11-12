from controller import *

class User(UserMixin, db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    userid = db.Column(db.Integer(), unique=True, autoincrement=False)
    password =db.Column(db.String(12), nullable=False)
    roleid=db.Column(db.Integer(), unique=False, nullable=False, autoincrement=False)

    def __init__(self, userid, password, roleid):
        self.userid = userid
        self.password = password
        self.roleid= roleid

    def __repr__(self):
        return '<User %r>' % self.id

    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.id)

class Member(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    memberid = db.Column(db.Integer(), unique=True, autoincrement=False)
    fname = db.Column(db.String(30), nullable=False)
    mname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    course = db.Column(db.String(30), nullable=False)
    orgCode = db.Column(db.String(4), nullable=False)

    def __init__(self, id, memberid, fname, mname, lname, course, orgCode):
        self.id = id
        self.memberid=memberid
        self.fname=fname
        self.mname=mname
        self.lname=lname
        self.course=course
        self.orgCode=orgCode

    def __repr__(self):
        return '<Member %r>' % self.id