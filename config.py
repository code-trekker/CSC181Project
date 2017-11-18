from flask import Flask
from flask.ext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '4321'
app.config['MYSQL_DATABASE_DB'] = 'pythonprogramming'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['SECRET_KEY'] = 'secret'

mysql.init_app(app)
