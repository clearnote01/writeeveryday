from flask import Flask, render_template, redirect, url_for, request, flash, session, g
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from rdb import db
from model import User
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

# Initialize app
app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.secret_key = "some_key"
db.init_app(app)
Scss(app)
login_manager = LoginManager(app)
login_manager.login_view = "loginsignuppage"

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
    print('Page opened home page')
    print(current_user)
    if g.user.is_authenticated == False:
        return redirect(url_for('firstpage'))
    user = None
    print(g.user)
    return render_template('index.jade', user = user)

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
    return 'Created tables'

@app.route('/auth_signup', methods=['POST'])
def signup():
    # user = User(request.form.username, request.form.password, request.form.email)
    # User.session.add(user)
    # User.session.commit()
    name = request.form['username']
    password = request.form['password']
    email = request.form['email']
    user = User(name, password, email)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return redirect(url_for('homepage'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('firstpage'))


if __name__=='__main__':
    app.run()
