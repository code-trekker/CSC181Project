import sqlalchemy
from flask import Flask, render_template,request
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_login import *
from werkzeug.security import generate_password_hash, \
     check_password_hash

class User(object):
    def __init__(self, username, password):
        self.username = username
        #self.password=password
        self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)





def checking():
    User.check_password(request.form['password'])


def createdb():
    conn = create_engine('mysql://root:pass@localhost') # connect to server
    conn.execute("CREATE DATABASE IF NOT EXISTS flaskapp")
    conn.execute("USE flaskapp")

    def uname_pass():
        user=User(request.form['username'], request.form['password'])
        cur=conn.cursor()
        cur.execute("INSERT INTO User(username,password)Values(%s,%s)",(user.username,user.password))

        msg = "hooooray!!"
        return render_template('admin_land.html', msg=msg)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:pass@localhost/flaskapp'
db=SQLAlchemy(app)