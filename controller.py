import sqlalchemy
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import *


def createDB():
    engine = sqlalchemy.create_engine('mysql://root:4321@localhost') # connect to server
    engine.execute("CREATE DATABASE IF NOT EXISTS flaskapp") #create db
    engine.execute("USE flaskapp") # select new

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:4321@localhost/flaskapp'
db = SQLAlchemy(app)



