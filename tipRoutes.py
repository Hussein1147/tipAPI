import unicodedata
import sys, os,json
import stripe
from flask import Flask, jsonify, Response, request
from flask_security import auth_token_required, http_auth_required
from models import app, user_datastore,User,db,Transfers
from sqlalchemy.exc import IntegrityError,InvalidRequestError
#Should be false in production mode
app.config['PROPAGATE_EXCEPTIONS'] =True
stripe.api_key = 'sk_test_OM2dp9YnI2w5eNuUKtrxd56g'

@app.route('/dummy-api')
@auth_token_required
def dummyAPI():
    dict = {
        "Key1": "Value1",
        "Key2": "value2"
    }
    return jsonify(items=dict)

@app.route('/add_accounts',methods=['Post'])
def addCard():
    data = request.get_json(force=True)
    userEmail=unicodedata.normalize('NFKD', data['userEmail']).encode('ascii','ignore')
    userCardNumber=unicodedata.normalize('NFKD', data['userCardNumber']).encode('ascii','ignore')
    userExpMonth=unicodedata.normalize('NFKD', data['userExpMonth']).encode('ascii','ignore')
    userExpYear=unicodedata.normalize('NFKD', data['userExpYear']).encode('ascii','ignore')
    try:    
            c1 = User.query.filter(User.email == userEmail).one()
            ##creating tokens
            token1 = stripe.Token.create(
            card={
                "number":userCardNumber,
                "exp_month":userExpMonth,
                "exp_year": userExpYear,
                'default_for_currency' : 'true',
                'currency' : 'usd'
                },
                )
        
            token2 = stripe.Token.create(
            card={
                "number": userCardNumber,
                "exp_month":userExpMonth,
                "exp_year": userExpYear,
                'default_for_currency' : 'true',
                'currency' : 'usd'
                },
                )
            des = "Customer for"+" "+ userEmail
            cus1 = stripe.Customer.create(
            description =des,
            source=token1.id
            )
            ##setting up stripe account
            stpacc1 = stripe.Account.create(
            country='US',
            managed=True,
            email = userEmail,
            external_account = token2.id,
            )
            c1.stpak = stpacc1.id
            c1.custid = cus1.id
            db.session.add(c1)
            db.session.commit()
            return jsonify(
            success = True,
            data = {
            'msg': 'Success!! created User!',
            }
            )
        
    except IntegrityError, e:
        db.session.rollback()
        return Response(e)
    except InvalidRequestError, e:
        db.session.rollback()
        return Response(e)    

@app.route('/tip', methods = ['POST'])
def tip():
    data = request.get_json(force=True)
    userEmail = unicodedata.normalize('NFKD', data['userEmail']).encode('ascii','ignore')
    receipientEmail = unicodedata.normalize('NFKD', data['repEmail']).encode('ascii','ignore')
    amt =  unicodedata.normalize('NFKD', data['amount']).encode('ascii','ignore')
    user1 = User.query.filter(User.email == userEmail).one()
    cust_id1 = user1.custid
    user2 = User.query.filter(User.email == receipientEmail).one()
    stpacc2 = user2.stpak
    try:
        charge = stripe.Charge.create(
            description="test.py",
            amount = amt,
            currency = "usd",
            customer= cust_id1,
            destination = stpacc2
            )
        emailKey = ""+ userEmail+""
        trnasferID = charge.transfer
        transfer= Transfers(stpkey = trnasferID, amount = (int(charge.amount)/10), email = userEmail, user_id= user1.id)
        db.session.add(transfer)
        db.session.commit()
        return jsonify(
            success = True,
            data = {
            'msg': 'Success!! User has been tipped!',
            }
            )
    except stripe.error.CardError, e:
        body = e.json_body
        err  = body['error']
        return Response(json.dumps(err))
    except stripe.error.InvalidRequestError, e:
         body = e.json_body
         err  = body['error']
         return Response(json.dumps(err))
         
@app.route('/create_user', methods=['POST'])
def createUser():
    data = request.get_json(force=True)
    userName = unicodedata.normalize('NFKD', data['userName']).encode('ascii','ignore')
    userPassword = unicodedata.normalize('NFKD', data['userPassword']).encode('ascii','ignore')
    userEmail= unicodedata.normalize('NFKD', data['userEmail']).encode('ascii','ignore')

    try:
        if User.query.filter(User.email == userEmail).first() is  None: 
            user_datastore.create_user(first_name=userName,email=userEmail, password= userPassword)
            db.session.commit()
            return jsonify(
            success = True,
            data = {
            'msg': 'Success!! created User!',
             }
            )        
        else:
            return Response(json.dumps("User email is taken!"))
            
    except IntegrityError, e:
        db.session.rollback()
        return Response(e)
    except InvalidRequestError, e:
        db.session.rollback()
        return Response(e)
if __name__ == '__main__':
    app.run()
