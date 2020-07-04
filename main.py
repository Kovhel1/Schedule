import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import  FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required, Email

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'very secret'
app.config['SQLALCHEMY_DATABASE_URI']=\
    'sqlite:///' + os.path.join(basedir, 'users.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config[ 'SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User (db.Model):
    __tabelname__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))
    email = db.Column(db.String(64), unique = True )
 
    
class Login(FlaskForm):
    username = StringField('Enter your username', validators = [Required()])
    password = PasswordField('Enter your password', validators = [Required()])
    email = StringField('your@mail.ru', validators = [Required(), Email()])
    submit = SubmitField('Submit')
    
    
    
    
    
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user/<name>')
def user(name):
    return render_template ('user.html', name=name)

@app.route('/login')
def login():
    return render_template ('login.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.route('/error/404')
def error_404():
    return render_template('404.html')

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')
        
@app.route('/error/500')
def error_500():
    return render_template('500.html')




if __name__ == '__main__':
    app.run(debug=True)
