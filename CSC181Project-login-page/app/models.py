from controller import *

class User(db.Model):
    id=db.Column(db.Integer(),primary_key=True, autoincrement=True)
    userid = db.Column(db.String(20), unique=True)
    password =db.Column(db.String(100), nullable=False)

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
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    memberid = db.Column(db.Integer(), unique=True, autoincrement=False)
    fname = db.Column(db.String(30), nullable=False)
    mname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    course = db.Column(db.String(30), nullable=False)
    orgCode = db.Column(db.String(4), nullable=False)

    def __repr__(self):
        return '<Member %r>' % self.id