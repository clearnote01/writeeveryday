from flask import Flask, render_template, redirect, url_for, request, flash, session, g
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from rdb import db
from model import User, Post, DbInfo
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from threading import Timer
from apscheduler.schedulers.background import BackgroundScheduler
import time
import json

# Initialize app
app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.secret_key = "some_key"
db.init_app(app)
Scss(app)
login_manager = LoginManager(app)
login_manager.login_view = "loginsignuppage"

def time_now():
    return time.localtime().tm_mday

def _shed():
    global today
    now = time_now()
    if now!=today:
        today = now
        import requests 
        url = 'http://localhost:5000/updateday'
        requests.get(url)
    print('Hallelujah')

@app.route('/updateday')
def updateDatabaseEODay():
    dbinfo = DbInfo.query.all()
    dbinfo = dbinfo[0]
    print(dbinfo)
    now = time_now()
    print('Now', now)
    print('last updated', dbinfo.last_updated)
    if now!=dbinfo.last_updated:
        dbinfo.last_updated = now
        db.session.commit()
        print('Updating data bas!! ! ! ! !')
        users = User.query.all()
        for user in users:
            user.day += 1
            db.session.commit()
    else:
        print('Won\'t update database')
    return redirect('/users')

s = BackgroundScheduler()
s.add_job(_shed,'interval', seconds=3600)
s.start()

@app.route('/users')
def all_users():
    users = User.query.all()
    u = str([user.__repr__() for user in users])
    return u


# Timer(3, updateDatabaseEODay, users).start()

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# EndInitialize

@app.before_request
def before_request():
    g.user = current_user
# Routes
@app.route('/')
def homepage():
    users = User.query.all()
    print('Page opened home page')
    print(current_user)
    if g.user.is_authenticated == False:
        return redirect(url_for('firstpage'))
    user = None
    print(g.user)
    return render_template('index.jade', user = g.user)

# simulate effect of posting on next day
@app.route('/nextday')
@login_required
def next_day():
    g.user.day += 1
    db.session.commit()
    return 'Current day of user' + str(g.user.day)

@app.route('/post/<day>')
@login_required
def view_post(day):
    post = Post.query.filter_by(user_id=g.user.id, day=day).first()
    print(post)
    if post == None:
        print('creating new post')
        post = Post(g.user, 'Empty page', day)
        print(post)
        db.session.add(post)
        db.session.commit()
    print(day, g.user)
    return str(post.text)

@app.route('/savepost', methods=['POST'])
@login_required
def savePage():
    print('Saving the page')
    text = request.data
    text = text.decode()
    print(text)
    postObject = json.loads(text)
    print(postObject["text"])
    post = Post.query.filter_by(user_id=g.user.id, day=postObject["day"]).first()
    print('Saving data in post: ', post)
    post.text = postObject["text"]
    post.words = postObject["words"]
    post.completed = postObject["completed"]
    db.session.commit()
    return 'success'
    
@app.route('/loginsignup')
def loginsignuppage():
    return render_template('loginpage.jade')
# Routes
@app.route('/welcome')
def firstpage():
    return render_template('first.jade')

@app.route('/auth_login', methods=['POST'])
def login():
    print(request.form)
    uname = request.form['username']
    upass = request.form['password']
    the_user = User.query.filter_by(username=uname).first()
    print(uname,upass)
    if the_user == None:
        error = 'USER NOT FOUND'
        flash(error)
        print(error)
        return redirect('/loginsignup')
    print(the_user, the_user.username, the_user.password)
    if the_user.password == upass:
        msg = 'PASSWORD MATCH'
        flash(msg)
        login_user(the_user)
        return redirect('/' or request.args.get('next'))
    else:
        msg = 'PASSWORD not match'
        flash(msg)
        return redirect('/loginsignup')

@app.route('/api/ct')
def create_db():
    db.create_all()
    datainfo = DbInfo(time_now(), 'root', 'root')
    db.session.add(datainfo)
    db.session.commit()
    print(datainfo) 
    return 'Created tables'

@app.route('/api/dt')
def destroy_db():
    db.drop_all()
    return 'Destroyed tables'

@app.route('/auth_signup', methods=['POST'])
def signup():
    # user = User(request.form.username, request.form.password, request.form.email)
    # User.session.add(user)
    # User.session.commit()
    name = request.form['username']
    password = request.form['password']
    email = request.form['email']
    try:
        user = User(name, password, email)
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print(e)
        flash('Some error occured')
        return redirect('/loginsignup')
    login_user(user)
    return redirect(url_for('homepage'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('firstpage'))


if __name__=='__main__':
    today = time_now()
    app.run()
