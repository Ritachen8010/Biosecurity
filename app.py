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

@app.route('/agro_home')
def agro_home():
    return render_template('3_agro_home.html')

@app.route('/agro_profile', methods=['GET', 'POST'])
def agro_profile():
    # check if loggined
    if 'loggedin' in session:
        # login and fetch details
        cursor = getCursor()
        cursor.execute('SELECT * FROM agro WHERE user_id = %s', (session['id'],))
        agro_info = cursor.fetchone()

        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            address = request.form['address']
            phone_num = request.form['phone_num']
            email = request.form['email']
            current_password = request.form['currentPassword']
            new_password = request.form['newPassword']
            confirm_password = request.form['confirmPassword']

            # verify password
            cursor.execute('SELECT password FROM user WHERE id = %s', (session['id'],))
            stored_password = cursor.fetchone()[0]
            if not hashing.check_value(stored_password, current_password, salt='8010'):
                # if password incorect
                return render_template('agro_profile.html', msg='Current password is incorrect.', agro=agro_info)

            # check old password and new password
            if new_password != confirm_password:
                return render_template('agro_profile.html', msg='New password and confirm password do not match.', agro=agro_info)

            # updated user and password
            hashed_new_password = hashing.hash_value(new_password, salt='8010')
            cursor.execute('UPDATE agro SET first_name=%s, last_name=%s, address=%s, phone_num=%s WHERE user_id=%s',
                           (first_name, last_name, address, phone_num, session['id']))
            cursor.execute('UPDATE user SET email=%s, password=%s WHERE id=%s', (email, hashed_new_password, session['id']))
            connection.commit()
            
            # updated in session
            session['email'] = email
            
            return redirect(url_for('agro_profile'))

        return render_template('3_agro_profile.html', agro=agro_info)
    return redirect(url_for('login'))

@app.route('/staff/home')
def staff_home():
    return render_template('4_staff_home.html')

@app.route('/staff/profile')
def staff_profile():
    return render_template('4_staff_profile.html')

@app.route('/admin/home')
def admin_home():
    return render_template('5_admin_home.html')

@app.route('/admin/profile')
def admin_profile():
    return render_template('5_admin_profile.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        first_name = request.form.get('first_name') # .get() for KeyError
        last_name = request.form.get('last_name')   # .get() for KeyError
        phone_number = request.form.get('phone_number') # .get() for KeyError
        address = request.form.get('address')
        role = 'agronomist'  # defult agronomist when register
        

        cursor = getCursor()

        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
        account = cursor.fetchone()

        # Check if email exists using MySQL
        cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
        email = cursor.fetchone()
        
        # If email exists show error and validation checks
        if email:
            msg = 'This email address is already registered. Please use a different email or login.'

        # If account exists show error and validation checks
        elif account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email or not first_name or not last_name:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            password = hashing.hash_value(password, salt='8010')
            # Insert data to user table
            cursor.execute('INSERT INTO user (username, password, email, role) VALUES (%s, %s, %s, %s)', (username, password, email, role))
            user_id = cursor.lastrowid

            # Insert data to agro table
            cursor.execute('INSERT INTO agro (user_id, first_name, last_name, phone_num, address, date_joined) VALUES (%s, %s, %s, %s, %s, CURDATE())', 
                            (user_id, first_name, last_name, phone_number, address))

            # For data change
            connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('6_register.html', msg=msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        input_password = request.form['password']  # Use a different variable name to avoid confusion
        
        # Get user data from MySQL
        cursor = getCursor()
        cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
        user = cursor.fetchone()

        if user:
            stored_password = user[2]  # Extract the stored hashed password

            # Check if the hashed input password matches the stored hashed password
            if hashing.check_value(stored_password, input_password, salt='8010'):
                print("Password verification succeeded.")
                session['loggedin'] = True
                session['id'] = user[0]
                session['username'] = user[1]
                session['email'] = user[3]
                session['role'] = user[4]

                # Redirect to a different dashboard based on the user's role
                if user[4] == 'agronomist':
                    return redirect(url_for('agro_home'))
                elif user[4] == 'staff':
                    return redirect(url_for('staff_home'))
                elif user[4] == 'admin':
                    return redirect(url_for('admin_home'))
                else:
                    return redirect(url_for('home'))
            else:
                # If the password is incorrect, update the message
                msg = 'Incorrect password!'
        else:
            # If the account doesn't exist or the username is incorrect, update the message
            msg = 'Incorrect username or account does not exist.'

    # Show the login form with the message (if any)
    return render_template('7_login.html', msg=msg)


@app.route('/weed_list')
def weed_list():
    return render_template('9_weed_list.html')

@app.route('/pest_list')
def pest_list():
    return render_template('10_pest_list.html')

