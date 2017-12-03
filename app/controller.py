import sqlalchemy
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import *
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password271997@localhost/purity'
#app.config['SECRET_KEY'] = 'seulrene'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['USE_SESSION_FOR_NEXT'] = True
app.secret_key = 'seulrene'
app.debug = True
db = SQLAlchemy(app)
Bootstrap(app)


def createDB():
    engine = sqlalchemy.create_engine('mysql://root:password271997@localhost')# connects to server
    engine.execute("CREATE DATABASE IF NOT EXISTS purity") #create db
    engine.execute("USE purity") # select new

def createTables():
    db.create_all()

