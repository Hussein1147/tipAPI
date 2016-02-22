import os
import unittest
import stripe
from flask import Flask
from models import User,Base,db
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()


app = Flask(__name__)

class TestCase(unittest.TestCase):

    def setUp(self):
        stripe.api_key = 'sk_test_OM2dp9YnI2w5eNuUKtrxd56g'
        db.drop_all()
        db.create_all()

    def addCard(self):
        u1 = User(first_name='Djibril',email='Djibrilhms@gmail.com', password='xyzhv')
        c1 = Card(CardNumber='4000056655665556',expYear='2017',expMonth='12',User_id=u1.id)
        db.session.add(c1)
        db.session.add(u1)
        db.session.commit()
        self.assertIsNotNone(c1)

    def testTransfers(self):
        u1 = User(first_name='Djibril',email='Djibril@gmail.com', password='xyzhv')
        u2 = User(first_name='Djibril',email='Djibril@live.com', password='xyzhv')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        
        token1 = stripe.Token.create(
            card={
                "number":'4000056655665556',
                "exp_month":'11',
                "exp_year": '2021',
                'default_for_currency' : 'true',
                'currency' : 'usd'
                },
                )
        
        token2 = stripe.Token.create(
            card={
                "number":'4000056655665556',
                "exp_month":'11',
                "exp_year": '2021',
                'default_for_currency' : 'true',
                'currency' : 'usd'
                },
                )
        token3 = stripe.Token.create(
            card={
                "number":'4000056655665556',
                "exp_month":'11',
                "exp_year": '2020',
                'default_for_currency' : 'true',
                'currency' : 'usd'
                },
                )     
      	self.assertIsNotNone(token1.id)
       	self.assertIsNotNone(token2.id)
        
        cus1 = stripe.Customer.create(
        description ="Customer for test@example.com",
        source=token1.id
        )
        self.assertIsNotNone(cus1.id)
        u1.custid = cus1.id
        print u1.custid
        self.assertIsNotNone(u1.custid)
        ##setting up transfer
        stpacc1 = stripe.Account.create(
        country='US',
        managed=True,
        email = 'djibril@gmail.com',
        external_account = token2.id,
        )
        u1.stpak = stpacc1.id
        self.assertIsNotNone(u1.stpak)
        print u1.stpak
        stpacc2 = stripe.Account.create(
        country='US',
        managed=True,
        email = 'djibril@gmail.com',
        external_account = token3.id,
        )
        ##creating charge
        charge = stripe.Charge.create(
            description="test.py",
            amount = '3000',
            currency = "usd",
            customer= cus1.id,
            destination = stpacc2.id
            )
    
        
        print charge
        # self.assertIsNotNone(transfer.id)

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

    def reCreate(self):
        db.create_all()
if __name__ == '__main__':
    unittest.main()
