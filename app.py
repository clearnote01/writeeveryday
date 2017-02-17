from flask import Flask, render_template
from flask_scss import Scss

# Initialize app
app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
Scss(app)
# EndInitialize

# Routes
@app.route('/')
def homepage():
    return render_template('index.jade')

# Routes
@app.route('/welcome')
def firstpage():
    return render_template('first.jade')

@app.route('/login', methods=['POST'])
def login():
    return 'Logged in!'

if __name__=='__main__':
    app.run()
