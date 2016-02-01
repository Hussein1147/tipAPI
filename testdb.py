import os
import unittest
from flask import Flask
from models import User,db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine,orm
from sqlalchemy.orm import sessionmaker,scoped_session


app = Flask(__name__)

class TestCase(unittest.TestCase):
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://adminVu2uiWr:AtZ6dRthSnWt@ 127.0.0.1:59891/tip'
    app.config['TESTING'] = True
    def setUp(self):
        db.create_all()

