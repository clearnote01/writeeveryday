from rdb import db
from datetime import datetime

if __name__=='__main__':
    from app import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id',db.Integer , primary_key=True)
    username = db.Column('username', db.String(20), unique=True , index=True)
    password = db.Column('password' , db.String(10))
    email = db.Column('email',db.String(50),unique=True , index=True)
    registered_on = db.Column('registered_on' , db.DateTime)
    day = db.Column('day', db.Integer)
    post = db.relationship('Post', backref='user', lazy='dynamic')
 
    def __init__(self , username ,password , email):
        self.username = username
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()
        self.day = 1
 
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return self.id
 
    def __repr__(self):
        return '[User {}: Day: {}]'.format(self.username, self.day)

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column('post_id', db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    completed = db.Column('completed', db.Integer)
    text = db.Column('post_text', db.String(10000))
    day = db.Column('post_day', db.Integer)

    def __init__(self, user, text, day, words=0, completed=0):
        self.user = user 
        self.text = text
        self.day = day 
        self.completed = completed

    def __repr__(self):
        return '[ Post: Day: {} : {} ]'.format(self.day, self.text)

class DbInfo(db.Model):
    __tablename__ = "dbinfo"
    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.Integer)
    root_name = db.Column(db.String(50))
    root_pass = db.Column(db.String(50))

    def __repr__(self):
        return '[Database: last_updated: {} root: {}'.format(self.last_updated, self.root_name)

    def __init__(self, time_here, root_u, root_p):
        self.last_updated = time_here 
        self.root_name = root_u
        self.root_pass = root_p 

if __name__=='__main__':
    db.create_all()
