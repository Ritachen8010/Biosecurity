from app import app
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

@app.route('/agro/home')
def agro_home():
        # check if loggined
    if 'loggedin' in session:
        # login and fetch details
        cursor = getCursor()
        cursor.execute('SELECT * FROM agro WHERE user_id = %s', (session['id'],))
        agro_info = cursor.fetchone()
        print("Agro Info:", agro_info)

        cursor.close()

    return render_template('3_agro_home.html', agro=agro_info)

@app.route('/agro/pest')
def agro_pest():
        # check if loggined
    if 'loggedin' in session:
        # login and fetch details
        cursor = getCursor()
        cursor.execute('SELECT * FROM agro WHERE user_id = %s', (session['id'],))
        agro_info = cursor.fetchone()
        print("Agro Info:", agro_info)

        cursor.close()

    return render_template('3_agro_pest.html')

@app.route('/agro/weed')
def agro_weed():
        # check if loggined
    if 'loggedin' in session:
        # login and fetch details
        cursor = getCursor()
        cursor.execute('SELECT * FROM agro WHERE user_id = %s', (session['id'],))
        agro_info = cursor.fetchone()
        print("Agro Info:", agro_info)

        cursor.close()

    return render_template('3_agro_weed.html')

@app.route('/agro/profile', methods=['GET', 'POST'])
def agro_profile():
    connection = getConnection()
    # check if loggined
    if 'loggedin' in session:
        # login and fetch details
        cursor = getCursor()
        cursor.execute('SELECT * FROM agro WHERE user_id = %s', (session['id'],))
        agro_info = cursor.fetchone()
        print("Agro Info:", agro_info)

        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            address = request.form['address']
            phone_num = request.form['phone_num']
            email = request.form['email']
            current_password = request.form['currentPassword']
            new_password = request.form['newPassword']
            confirm_password = request.form['confirmPassword']
            print("Form Data - First Name:", first_name)
            print("Form Data - Last Name:", last_name)
            print("Form Data - Address:", address)
            print("Form Data - Phone Number:", phone_num)
            print("Form Data - Email:", email)
            print("Form Data - Current Password:", current_password)
            print("Form Data - New Password:", new_password)
            print("Form Data - Confirm Password:", confirm_password)


            # check if the new email already exists
            cursor.execute('SELECT * FROM user WHERE email = %s AND user_id != %s', (email, session['id']))
            existing_user = cursor.fetchone()
            if existing_user:
                # if the email already exists
                return render_template('3_agro_profile.html', 
                           msg='The email is already in use.', 
                           msg_type='error',
                           agro=agro_info)
            
            # verify password
            cursor.execute('SELECT password FROM user WHERE user_id = %s', (session['id'],))
            stored_password = cursor.fetchone()[0]
            if not hashing.check_value(stored_password, current_password, salt='8010'):
                # if password incorect
                return render_template('3_agro_profile.html', 
                                       msg='Current password is incorrect.', 
                                       msg_type='error',
                                       agro=agro_info)

            # check old password and new password
            if new_password and confirm_password:
                if new_password != confirm_password:
                    return render_template('3_agro_profile.html', 
                                           msg='New password and confirm password do not match.', 
                                           msg_type='error',
                                           agro=agro_info)
                hashed_new_password = hashing.hash_value(new_password, salt='8010')
                # update password
                cursor.execute('UPDATE user SET password=%s WHERE user_id=%s', (hashed_new_password, session['id']))


            # update other user information
            cursor.execute('UPDATE agro SET first_name=%s, last_name=%s, address=%s, phone_num=%s WHERE user_id=%s',
                           (first_name, last_name, address, phone_num, session['id']))
            print('UPDATE agro SET first_name=%s, last_name=%s, address=%s, phone_num=%s WHERE user_id=%s' % 
                  (first_name, last_name, address, phone_num, session['id']))
            cursor.execute('UPDATE user SET email=%s WHERE user_id=%s', (email, session['id']))
            print('UPDATE user SET email=%s WHERE user_id=%s' % (email, session['id']))
            print("Before commit")
            connection.commit()
            print("After commit")
            
            print("Updating user and agro table...")
            
            # updated in session
            session['email'] = email
            print("New email:", email)
            
            return render_template('3_agro_profile.html', 
                                   msg='Profile updated successfully.', 
                                   msg_type='success',
                                   agro=agro_info)

        return render_template('3_agro_profile.html', agro=agro_info)
    return redirect(url_for('login'))