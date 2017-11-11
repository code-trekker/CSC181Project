from flask_sqlalchemy import SQLAlchemy
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:4321@localhost/tests'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Member(db.Model):
    student_id=db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(25), nullable=False)
    mname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    course = db.Column(db.String(25), nullable=False)

    def __init__(self, student_id, fname, mname, lname, course):
        self.student_id = student_id
        self.fname=fname
        self.mname=mname
        self.lname=lname
        self.course=course