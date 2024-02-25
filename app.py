from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import connect
from flask_hashing import Hashing

app = Flask(__name__)
hashing = Hashing(app)  #create an instance of hashing

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = '8010'

dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, auth_plugin='mysql_native_password',\
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

@app.route('/')
def home():
    return render_template('1_home.html')

@app.route('/about_us')
def about_us():
    return render_template('2_about_us.html')

@app.route('/agro')
def agro():
    return render_template('3_agro.html')

@app.route('/staff')
def staff_home():
    return render_template('4_staff.html')

@app.route('/admin')
def admin_home():
    return render_template('5_admin.html')

@app.route('/register')
def register():
    return render_template('6_register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Get user data from MySQL
        cursor = getCursor()
        cursor.execute('SELECT user_id, username, password, role FROM user WHERE username = %s', (username,))
        user = cursor.fetchone()

        if hashing.check_value(user[2], password, salt='8010'):
            session['loggedin'] = True
            session['id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[4]
            # Directed to a different dashboard.
            if user[4] == 'agronomist':
                return redirect(url_for('agro'))
            elif user[4] == 'staff':
                return redirect(url_for('staff'))
            elif user[4] == 'admin':
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('home'))
        else:
            # Account doesnt exist or username incorrect
            msg = 'Incorrect username'
    # Show the login form with message (if any)
    return render_template('7_login.html', msg=msg)

@app.route('/profile')
def profile():
    return render_template('8_profile.html')