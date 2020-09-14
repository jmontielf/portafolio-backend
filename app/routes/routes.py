from flask import Flask, render_template, request
from flask_mysqldb import MySQL

routes = Flask(__name__)

routes.config['MYSQL_HOST'] = ''
routes.config['MYSQL_USER'] = ''
routes.config['MYSQL_PASSWORD'] = ''
routes.config['MYSQL_HOST'] = ''

mysql = MySQL(routes)

@routes.route('/')
def index():
    return render_template('sign-up.html')

@routes.route('/signup', method=['POST'])
def sign_up():
    if request.method == 'POST':
        request.form['suser']
        request.form['spassword']

if __name__ == '__main__':
    routes.run(port = 3000, debug = True)