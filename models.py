from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://56aee17b0c1e66574300003d-jobos.rhcloud.com:59891'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

     
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

db.create_all()