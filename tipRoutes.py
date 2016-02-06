import unicodedata
import sys, os
from flask import Flask, jsonify, Response, request
from flask_security import auth_token_required, http_auth_required
from models import app, user_datastore,User,db
from sqlalchemy.exc import IntegrityError,InvalidRequestError
#Should be false in production mode
app.config['PROPAGATE_EXCEPTIONS'] =True

@app.route('/dummy-api')
@auth_token_required
def dummyAPI():
    dict = {
        "Key1": "Value1",
        "Key2": "value2"
    }
    return jsonify(items=dict)
    

@app.route('/create_user', methods=['POST'])
def createUser():
    data = request.get_json(force=True)
    userName = unicodedata.normalize('NFKD', data['username']).encode('ascii','ignore')
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