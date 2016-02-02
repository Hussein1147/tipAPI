import json
from flask import Flask
from flask.ext.security import Security, SQLAlchemyUserDatastore,UserMixin, RoleMixin, login_required
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://adminVu2uiWr:AtZ6dRthSnWt@127.0.0.1:59892/tip'
app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
app.config['SECURITY_PASSWORD_SALT'] = 'requiem_for_a_dream'
app.config['SECURITY_TRACKABLE'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
role_users = db.Table('roles_users',db.Column('user_id', db.Integer(), db.ForeignKey('auth_user.id')),db.Column('role_id', db.Integer(), db.ForeignKey('auth_role.id')))

class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer(), primary_key=True)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())
    modified_at = db.Column(db.DateTime(), default = datetime.utcnow())

class Role(Base, RoleMixin):
    __tablename__ ='auth_role'
    name = db.Column(db.String(80), nullable = False, unique =True)
    description = db.Column(db.String(255))
    
    def __init__ (self, name):
        self.name = name
        
    def __repr__ (self):
        return '<Role %r>' % self.name
  
class User(Base,UserMixin):
    __tablename__ = 'auth_user'
    
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    def __repr__(self):
        return '<User %>' % self.email

user_datastore = SQLAlchemyUserDatastore(db, User,Role)
security = Security(app, user_datastore)
db.create_all()
@app.before_first_request
def create_user():
    db.create_all()
    if not User.query.first():
        user_datastore.create_user(email='test@example.com', password='test123')
        db.session.commit()