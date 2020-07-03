import os
from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']=\
    'sqlite:///' + os.path.join(basedir, 'users.sqlite')


@app.route('/')
def index():
    return render_template('index.html')




@app.route('/user/<name>')
def user(name):
    return render_template ('user.html', name=name)


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
