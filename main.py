import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import  FlaskForm
from flask_bootstrap import Bootstrap
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
bootstrap = Bootstrap(app)

class User (db.Model):
    __tabelname__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))
    email = db.Column(db.String(64) )
    
    def __repr__(self):
        return '<User %r>' % self.username

    
    
class Login(FlaskForm):
    username = StringField('Username', validators = [Required()])
    password = PasswordField('Password', validators = [Required()])
    email = StringField('Email', validators = [Required(), Email()])
    submit = SubmitField('Submit')
    
    
    
    
    
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user/<username>')
def user(username):
    return render_template ('user.html', username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            mail = User.query.filter_by(email=form.email.data).first()
            if mail is None:
                user = User(username=form.username.data, email=form.email.data, password=form.password.data )
                db.session.add(user)
                session['username'] =  form.username.data
                form.username.data = ''
                return render_template ( 'user.html', username=session.get('username') )
            else:
                flash('This mail exists.Inter another mail')
                return render_template ( 'login.html', form=form )
        else:
            flash('This user exists. If you loose your password or login..')
            return render_template ( 'login.html', form=form )
    return render_template ( 'login.html', form=form,  username=session.get('username'), email=session.get('email'), password=session.get('password') )    

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
