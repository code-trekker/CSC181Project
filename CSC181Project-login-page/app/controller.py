import sqlalchemy
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import *
from sqlalchemy_utils import database_exists
from urlparse import urlparse, urljoin


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:pass@localhost/flaskapp'
#app.config['SECRET_KEY'] = 'seulrene'
app.config['USE_SESSION_FOR_NEXT'] = True
app.secret_key = 'seulrene'
app.debug = True
db = SQLAlchemy(app)


def createDB():
    engine = sqlalchemy.create_engine('mysql://root:pass@localhost')# connects to server
    engine.execute("CREATE DATABASE IF NOT EXISTS flaskapp") #create db
    engine.execute("USE flaskapp") # select new

def createTables():
    db.create_all()



