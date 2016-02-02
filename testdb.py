import os
import unittest
from flask import Flask
from models import User,Base,db



app = Flask(__name__)

class TestCase(unittest.TestCase):

    def setUp(self):
        db.drop_all()
        db.create_all()


    def testUser(self):
        u1 = User(first_name='Djibril',email='Djibrilhms@gmail.com', password='xyzhv')
        db.session.add(u1)
        db.session.commit()
        self.assertIsNotNone(u1)
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    def trunCate(self):
        db.drop_all()
        db.create_all()
        
if __name__ == '__main__':
    unittest.main()