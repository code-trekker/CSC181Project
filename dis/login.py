import sqlalchemy
from werkzeug.security import generate_password_hash,check_password_hash
from flask import Flask, render_template,request,session
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_login import *
from werkzeug.security import generate_password_hash, \
     check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:pass@localhost/flaskapp123'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)


def createdb():
    conn = create_engine('mysql://root:pass@localhost') # connect to server
    conn.execute("CREATE DATABASE IF NOT EXISTS flaskapp123")
    conn.execute("USE flaskapp")

def createTables():
    db.create_all()

class User(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.String(9),nullable = False, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    passwd = db.Column(db.String(200), nullable=False)

    def __init__(self,id,username,passwd):
        self.id=id
        self.username = username
        self.passwd= generate_password_hash(passwd)



    def set_password(self, passwd):
        self.pw_hash = generate_password_hash(passwd)

    def check_password(self, passwd):
        return check_password_hash(self.pw_hash, passwd)

class viewer(db.Model):
    __tablename__= "viewer"
    id = db.Column(db.String(9), nullable=False, primary_key=True)








    '''def uname_pass():
        user=User(request.form['username'], request.form['password'])
        cur=conn.cursor()
        cur.execute("INSERT INTO User(username,password)Values(%s,%s)",(user.username,user.password))

        msg = "hooooray!!"
        return render_template('admin_land.html', msg=msg)'''

