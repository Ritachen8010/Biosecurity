from app import app
from flask import flash
from flask import session
from flask import redirect
from flask import url_for
from flask import request
from flask import render_template
import mysql.connector
from app.database import getCursor
from app.database import getConnection
from app import connect
from app import hashing
import re


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        input_password = request.form['password'] 
        
        # Get user data from MySQL
        cursor = getCursor()
        cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
        user = cursor.fetchone()

        if user:
            stored_password = user[2]  # Extract the stored hashed password

            # Check if the hashed input password matches the stored hashed password
            if hashing.check_value(stored_password, input_password, salt='8010'):
                print('Hashing instance created')

                # Check if the user's status is active
                if user[5] == 'active':
                    session['loggedin'] = True
                    session['id'] = user[0]
                    session['username'] = user[1]
                    session['email'] = user[3]
                    session['role'] = user[4]
                    session['status'] = user[5]

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
                    msg = 'Your account is inactive.'
            else:
                msg = 'Incorrect password!'
        else:
            msg = 'Incorrect username or account does not exist.'

    return render_template('7_login.html', msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        first_name = request.form.get('first_name', '') # .get() for KeyError
        last_name = request.form.get('last_name', '')
        phone_number = request.form.get('phone_number', '')
        address = request.form.get('address', '')
        role = 'agronomist'  # defult agronomist when register

        cursor = getCursor()
        connection = getConnection()

        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
        if cursor.fetchone():
            msg = 'Account already exists!'
        
        else:
            # check if eamil exsiting 
            cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
            if cursor.fetchone():
                msg = 'This email address is already registered. Please use a different email or login.'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            else:
                # insert new ueser
                hashed_password = hashing.hash_value(password, salt='8010')
                cursor.execute('INSERT INTO user (username, password, email, role) VALUES (%s, %s, %s, %s)',
                               (username, hashed_password, email, role))
                user_id = cursor.lastrowid
                cursor.execute('INSERT INTO agro (user_id, first_name, last_name, phone_num, address, date_joined) VALUES (%s, %s, %s, %s, %s, CURDATE())',
                               (user_id, first_name, last_name, phone_number, address))
                connection.commit()
                msg = 'You have successfully registered!'
                
    return render_template('6_register.html', msg=msg)

@app.route('/logout')
def logout():
    # remove session data, this will log the user out
    session.clear()
    # flash a message to the user
    flash('You have successfully logged out.', 'info') 
    # redirect to login page
    return redirect(url_for('login'))
