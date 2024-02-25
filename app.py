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


    return render_template('7_login.html')

@app.route('/profile')
def profile():
    return render_template('8_profile.html')