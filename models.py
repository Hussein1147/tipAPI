from flask import Flask
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://adminVu2uiWr:AtZ6dRthSnWt@127.0.0.1:59893/tip'
app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
app.config['SECURITY_PASSWORD_SALT'] = 'requiem_for_a_dream'
app.config['SECURITY_TRACKABLE'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['WTF_CSRF_ENABLED'] = False
app.config['SECRET_KEY'] = 'super secret key'
db = SQLAlchemy(app)

roles_users = db.Table('roles_users',db.Column('user_id', db.Integer(), db.ForeignKey('auth_user.id')),db.Column('role_id', db.Integer(), db.ForeignKey('auth_role.id')))

followers = db.Table('followers', db.Column('follower_id',db.Integer(),db.ForeignKey('auth_user.id')), db.Column('followed_id', db.Integer(), db.ForeignKey('auth_user.id')))
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
 
class User(Base, UserMixin):
    __tablename__ = 'auth_user'
       
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(45))
    current_login_ip = db.Column(db.String(45))
    login_count = db.Column(db.Integer)
    stpak = db.Column(db.String(255))
    custid = db.Column(db.String(255))
    authTok = db.Column(db.String(255))
    transfer= db.relationship('Transfers',backref='auth_user')
    roles = db.relationship('Role', secondary= roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    followed= db.relationship(
                             'User',
                             secondary= followers,
                             primaryjoin="followers.c.follower_id == User.id", 
                             secondaryjoin="followers.c.followed_id == User.id", 
                             backref=db.backref('followers', lazy='dynamic'), 
                             lazy='dynamic')
    
    def follow(self,user):
        if not self.is_following(user):
            self.followed.append(user)
        return self 
    
    def get_followers(self):
        db.session.query(User.first_name,User.email).join(followers.c.followed_id == User.id).\
                filter(followers.c.follower_id == self.id).order_by(User.name.asc()).all()
   
    def unfollow(self,user):
        if self.is_following(user):
            self.followed.remove(user)
            return self
   
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id ==user.id).count() > 0
class Transfers(Base):
    __tablename__ = 'transfers'
    stpkey = db.Column(db.String(255))
    amount = db.Column(db.Integer)
    email =  db.Column(db.String(45))
    user_id= db.Column(db.Integer, db.ForeignKey('auth_user.id'))
db.create_all()
user_datastore = SQLAlchemyUserDatastore(db, User,Role)
security = Security()
security.init_app(app, user_datastore)
@app.before_first_request
def create_user():
    db.create_all()
   
