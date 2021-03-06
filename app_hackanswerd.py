from flask import Flask, render_template, session
from flask import flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import request
from models import User, UserTag, Question, QuestionTag, Answer
from rdb import db
from flask_babel import format_datetime,format_date,Babel
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin


app = Flask(__name__, static_url_path='/static')
app.secret_key = "some_key"
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'false'
db.init_app(app)
Babel(app)

#######################################################
#   Templates: 
#
#   first_page.html <- /
#   question.html <- /qs/<id>
#   questions.html <- /qs/all, my questions
#   answers.html <- my answers
#   profile.html <- /profile, /user/<uname>
#   new_question.html 
#
######################################################

login_manager = LoginManager(app)
class LogUser(UserMixin):
    def __init__(self, username):
        self.id = username

login_manager.login_view = "first_page"

@login_manager.user_loader
def load_user(id):
    return LogUser(id)

def reformat_date(date,format =None):
    return format_date(date,format)

# app.jinja_env.filters['datetime'] = reformat_date
# @app.route('/')
# def first_page():
    # return render_template('finalfirstpage.html')
# @app.route('/first_page')
# def welcome_page():
    # return render_template('first_page.html')

@app.route('/')
def index():
    return render_template('first_page.html')

@app.route('/welcome')
def welcome():
    return render_template('finalfirstpage.html')

@app.route('/about')
@login_required
def about_page():
    return render_template('aboutpage1.html')

@app.route('/login', methods = ['POST'])
def signin():
    print("GOT A POST OF DATA !!!")
    uname = request.form['uname']
    upass = request.form['upass']
    the_user = User.query.filter_by(uname=uname).first()
    print(uname,upass)
    if the_user == None:
        error = 'USER NOT FOUND'
        flash(error)
        return redirect('/')
    print(the_user, the_user.uname, the_user.upass)
    if the_user.upass == upass:
        msg = 'PASSWORD MATCH'
        session['user'] = uname
        user = LogUser(uname)
        login_user(user)
        return redirect('/user/{}'.format(uname))
    else:
        msg = 'PASSWORD not match'
    flash(msg)
    return redirect('/')

@app.route('/signup', methods = ['POST'])
def signup():
    user = User(request.form['uname'], request.form['upass'],
    request.form['email'], request.form['name'], request.form['roll_no'], request.form['branch'])

    print(user)
    db.session.add(user)
    db.session.commit()
    session['user'] = user.uname
    print('Record was successfully added')
    user = LogUser(uname)
    login_user(user)
    return redirect('/user/{}'.format(user.uname))

@app.route('/qs/recc')
@login_required
def reccomended():
    uname = session['user']
    user = User.query.filter_by(uname=uname).first_or_404()
    user_tags = user.usertags.all()
    lis = []
    user_tags_text = [u.name for u in user_tags]
    print('USER TAGS: ',user_tags_text)
    questions = Question.query.all()
    print('Questions: ', questions)
    for qs in questions:
        print(qs.question_tags.all())
        qs_tags =  qs.question_tags.all()
        for qs_tag in qs_tags:
            for tag in user_tags_text:
                if qs_tag.name == tag:
                    print('Matched question: ', qs.question_text)
                    lis.append(qs)
    lis = set(lis)
    print(lis)
    lis = list(lis)
    return render_template('questions_s.html', questions=lis)
    
@app.route('/all/users')
@login_required
def all_users():
    print('Value of session["user"]:', session['user'])
    print('All users page')
    users = User.query.all()
    print(users)
    return 'Users: {}'.format(len(users))

@app.route('/qs/topic/all')
@login_required
def all_topics():
    pass

@app.route('/qs/all')
@login_required
def all_questions():
    questions = Question.query.all()
    return render_template('questions_s.html', questions=questions)

@app.route('/qs/<id>', methods=['POST', 'GET'])
@login_required
def questions_page(id):
    print('PAGE OPENED: ', id)
    question = Question.query.filter_by(id=id).first_or_404()
    uname = session['user']
    user = User.query.filter_by(uname=uname).first()
    print(question.answers.all())
    if request.method == 'POST':
        answer_text = request.form['answer']
        answer = Answer(answer_text, user, question)
        print(answer.answer_text)
        db.session.add(answer)
        db.session.commit()
        print(question.answers.all())
    print(question.answers.all())
    return render_template('question_s.html', question=question)

@app.route('/profile')
@login_required
def profile_page_mine():
    uname = session['user']
    return redirect('/user/{}'.format(uname))

@app.route('/questions')
@login_required
def my_questions():
    uname = session['user']
    user = User.query.filter_by(uname=uname).first_or_404()
    print('Question: ',user)
    questions = user.questions.all()
    print(questions)
    return render_template('questions_s.html', questions = questions)
        
@app.route('/user/<uname>', methods=['POST', 'GET'])
@login_required
def profile_page(uname):
    user = User.query.filter_by(uname=uname).first_or_404()
    if request.method == 'POST':
        tag_name = request.form['tag']
        tag_new = UserTag(tag_name, user)
        db.session.add(tag_new)
        db.session.commit()
    return render_template('profile_sagar.html', user=user)

@app.route('/answers')
@login_required
def my_answers():
    uname = session['user']
    user = User.query.filter_by(uname=uname).first()
    answers = user.answers.all()
    return render_template('answers.html', answers=answers)

@app.route('/new_question', methods=['GET','POST'])
@login_required
def new_qs():
    if request.method == 'POST':
        print('SOmething POST')
        uname = session['user']
        user = User.query.filter_by(uname=uname).first()
        tags = request.form['tags']
        qs = request.form['question']
        qs_new = Question(qs, user)
        db.session.add(qs_new)
        tags = tags.split(',')
        for tag in tags:
            tag = tag.strip()
            tag = tag.lower()
            print(tag)
            tag_n = QuestionTag(tag, qs_new)
            db.session.add(tag_n)
        db.session.commit()
        print(qs_new)
    return render_template('askques.html')

@app.route('/api/ct')
def create_tables():
    db.create_all()
    return 'Created tables'

@app.route('/api/dt')
def destroy_tables():
    db.drop_all()
    return 'Destroyed tables'

@app.route('/logout')
@login_required
def logout():
    session['user'] = ''
    logout_user()
    return redirect('/')

if __name__=='__main__':
    app.run()
