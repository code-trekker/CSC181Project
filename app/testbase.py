from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
engine = sqlalchemy.create_engine('mysql://root:4321@localhost') # connect to server
#engine.execute("CREATE DATABASE IF NOT EXISTS dbname") #create db
#engine.execute("USE dbname") # select new

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:4321@localhost/dbname.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
