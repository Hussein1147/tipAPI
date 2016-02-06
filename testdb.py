import os
import unittest
from flask import Flask
from models import User,Base,db,Card



app = Flask(__name__)

class TestCase(unittest.TestCase):

    def setUp(self):
        db.drop_all()
        db.create_all()

    def addCard(self):
        u1 = User(first_name='Djibril',email='Djibrilhms@gmail.com', password='xyzhv')
        c1 = Card(CardNumber='4000000000000077',expYear='2017',expMonth='12',User_id=u1.id)
        db.session.add(c1)
        db.session.add(u1)
        db.session.commit()
        self.assertIsNotNone(c1)


    def testUser(self):
        u1 = User(first_name='Djibril',email='Djibrilhms@gmail.com', password='xyzhv')
        db.session.add(u1)
        db.session.commit()
        self.assertIsNotNone(u1)
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    # def trunCate(self):
    #     db.drop_all()
    # def reCreate(self):
    #     db.create_all()
if __name__ == '__main__':
    unittest.main()