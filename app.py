from flask import Flask
from flask import flash
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

@app.route('/agro/home')
def agro_home():
        # check if loggined
    if 'loggedin' in session:
        # login and fetch details
        cursor = getCursor()
        cursor.execute('SELECT * FROM agro WHERE user_id = %s', (session['id'],))
        agro_info = cursor.fetchone()
        print("Agro Info:", agro_info)

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

    return render_template('3_agro_weed.html')

@app.route('/agro/profile', methods=['GET', 'POST'])
def agro_profile():
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

@app.route('/staff/home')
def staff_home():
    if 'loggedin' in session:
        # login and fetch details
        cursor = getCursor()
        cursor.execute('SELECT * FROM staff_admin WHERE user_id = %s', (session['id'],))
        staff_info = cursor.fetchone()
        print("staff Info:", staff_info)

    return render_template('4_staff_home.html', staff_info=staff_info)

@app.route('/staff/edit_bio')
def staff_edit_bio():
    if 'loggedin' in session:
        # login and fetch details
        cursor = getCursor()
        cursor.execute('SELECT * FROM staff_admin WHERE user_id = %s', (session['id'],))
        staff_info = cursor.fetchone()
        print("staff Info:", staff_info)

    return render_template('4_staff_edit_bio.html', staff_info=staff_info)

@app.route('/staff/view_agro_profile')
def staff_view_agro():
    if 'loggedin' in session:
        # login and fetch details
        cursor = getCursor()
        cursor.execute('SELECT * FROM staff_admin WHERE user_id = %s', (session['id'],))
        staff_info = cursor.fetchone()
        print("staff Info:", staff_info)

        cursor.execute('''
            SELECT agro.agro_id, agro.first_name, agro.last_name, agro.address, 
            agro.phone_num, agro.date_joined, user.username, user.email, user.status
            FROM agro
            JOIN user ON agro.user_id = user.user_id
        ''')
        combined_list = cursor.fetchall()

    return render_template('4_staff_view_agro.html', combined_list=combined_list, staff_info=staff_info)

@app.route('/staff/profile', methods=['GET', 'POST'])
def staff_profile():
    # check if loggined
    if 'loggedin' in session:
        # login and fetch details
        cursor = getCursor()
        cursor.execute('SELECT * FROM staff_admin WHERE user_id = %s', (session['id'],))
        staff_info = cursor.fetchone()
        print("staff Info:", staff_info)

        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            phone_num = request.form['phone_num']
            email = request.form['email']
            current_password = request.form['currentPassword']
            new_password = request.form['newPassword']
            confirm_password = request.form['confirmPassword']
            print("Form Data - First Name:", first_name)
            print("Form Data - Last Name:", last_name)
            print("Form Data - Phone Number:", phone_num)
            print("Form Data - Email:", email)
            print("Form Data - Current Password:", current_password)
            print("Form Data - New Password:", new_password)
            print("Form Data - Confirm Password:", confirm_password)


            # verify password
            cursor.execute('SELECT password FROM user WHERE user_id = %s', (session['id'],))
            stored_password = cursor.fetchone()[0]
            if not hashing.check_value(stored_password, current_password, salt='8010'):
                # if password incorect
                return render_template('4_staff_profile.html', 
                                       msg='Current password is incorrect.', 
                                       msg_type='error',
                                       staff=staff_info)

            # check old password and new password
            if new_password and confirm_password:
                if new_password != confirm_password:
                    return render_template('4_staff_profile.html', 
                                           msg='New password and confirm password do not match.', 
                                           msg_type='error',
                                           staff=staff_info)
                hashed_new_password = hashing.hash_value(new_password, salt='8010')
                # update password
                cursor.execute('UPDATE user SET password=%s WHERE user_id=%s', (hashed_new_password, session['id']))


            # update other user information
            cursor.execute('UPDATE staff_admin SET first_name=%s, last_name=%s, address=%s, phone_num=%s WHERE user_id=%s',
                           (first_name, last_name, phone_num, session['id']))
            print('UPDATE staff_admin SET first_name=%s, last_name=%s, address=%s, phone_num=%s WHERE user_id=%s' % 
                  (first_name, last_name, phone_num, session['id']))
            cursor.execute('UPDATE user SET email=%s WHERE user_id=%s', (email, session['id']))
            print('UPDATE user SET email=%s WHERE user_id=%s' % (email, session['id']))
            print("Before commit")
            connection.commit()
            print("After commit")
            
            print("Updating user and staff table...")
            
            # updated in session
            session['email'] = email
            print("New email:", email)
            
            return render_template('4_staff_profile.html', 
                                   msg='Profile updated successfully.', 
                                   msg_type='success',
                                   staff=staff_info)

        return render_template('4_staff_profile.html', staff=staff_info)
    return redirect(url_for('login'))

@app.route('/admin/home')
def admin_home():
    # check if loggined
    if 'loggedin' in session:
        # login and fetch details
        cursor = getCursor()
        cursor.execute('SELECT * FROM staff_admin WHERE user_id = %s', (session['id'],))
        admin_info = cursor.fetchone()
        print("admin_info:", admin_info)

    return render_template('5_admin_home.html', admin=admin_info)

@app.route('/admin/manage_bio')
def admin_m_bio():
    return render_template('5_admin_manage_bio.html')

@app.route('/admin/manage_agro', methods=['GET', 'POST'])
def admin_m_agro():
    if 'loggedin' in session:
        # login and fetch details
        cursor = getCursor()
        cursor.execute('SELECT * FROM staff_admin WHERE user_id = %s', (session['id'],))
        admin_info = cursor.fetchone()
        print("admin_info:", admin_info)

        # get agro info
        cursor.execute('''
            SELECT agro.agro_id, agro.first_name, agro.last_name, agro.address, 
            agro.phone_num, agro.date_joined, user.username, user.email, user.status
            FROM agro
            JOIN user ON agro.user_id = user.user_id
        ''')
        combined_list = cursor.fetchall()

    return render_template('5_admin_manage_agro.html', combined_list=combined_list, admin=admin_info)   

@app.route('/admin/agronomists/update/<int:id>', methods=['GET', 'POST'])
def update_agro(id):
    cursor = getCursor()
    if request.method == 'POST':
        agro_id = request.form['agro_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address']
        phone_num = request.form['phone_num']
        email = request.form['email']
        status = request.form['status']
        print("Form data:", request.form)

        # updated date
        cursor.execute('UPDATE agro SET first_name=%s, last_name=%s, address=%s, phone_num=%s WHERE agro_id=%s',
                       (first_name, last_name, address, phone_num, agro_id))
        print('UPDATE agro SET first_name=%s, last_name=%s, address=%s, phone_num=%s WHERE agro_id=%s'
            % (first_name, last_name, address, phone_num, agro_id))
        cursor.execute('UPDATE user SET email=%s, status=%s WHERE user_id=(SELECT user_id FROM agro WHERE agro_id=%s)',
                        (email, status, agro_id))

        connection.commit()

        return redirect(url_for('admin_m_agro'))
    else:
        # get agro info
        cursor.execute('''
            SELECT agro.agro_id, agro.first_name, agro.last_name, agro.address, 
            agro.phone_num, agro.date_joined, user.username, user.email, user.status
            FROM agro
            JOIN user ON agro.user_id = user.user_id
            WHERE agro.agro_id = %s
        ''', (id,))
        agro = cursor.fetchone()

        return render_template('5_admin_manage_agro_edit.html', agro=agro)

@app.route('/add_agro', methods=['GET', 'POST'])
def add_agro():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address']
        phone_num = request.form['phone_num']
        date_joined = request.form['date_joined']
        username = request.form['username']
        password = request.form['password'] #raw password
        email = request.form['email']
        role = request.form['role']
        status = request.form['status']
        print("Form data:", request.form)

        # Check if username already exists
        cursor = getCursor()
        cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            msg = 'Account already exists!'
            return render_template('5_admin_manage_add_agro.html', msg=msg)

        # hash with salt
        hashed_password = hashing.hash_value(password, salt='8010')

        # insert new agro
        cursor = getCursor()
        cursor.execute('INSERT INTO agro (first_name, last_name, address, phone_num, date_joined) VALUES (%s, %s, %s, %s, %s)',
               (first_name, last_name, address, phone_num, date_joined))
        agro_id = cursor.lastrowid  # get new agro_id

        # insert new user
        cursor.execute('INSERT INTO user (username, password, email, role, status) VALUES (%s, %s, %s, %s, %s)',
               (username, hashed_password, email, role, status))
        user_id = cursor.lastrowid  # get new agro_id

        # update agro.user id
        cursor.execute('UPDATE agro SET user_id = %s WHERE agro_id = %s', (user_id, agro_id))
        connection.commit()

        # success flash message
        flash('Agro added successfully!', 'success')

        return redirect(url_for('admin_m_agro'))
    else:
        return render_template('5_admin_manage_add_agro.html')
    
@app.route('/delete_agro/<int:agro_id>', methods=['POST'])
def delete_agro(agro_id):
    cursor = getCursor()
    cursor.execute('SELECT agro.agro_id, agro.first_name, agro.last_name, agro.address, agro.phone_num, agro.date_joined, user.user_id, user.username, user.password, user.email, user.role, user.status FROM agro JOIN user ON agro.user_id = user.user_id WHERE agro.agro_id = %s', (agro_id,))
    agro = cursor.fetchone()

    try:
        # delete from agro
        cursor.execute('DELETE FROM agro WHERE agro_id = %s', (agro_id,))
        # delete from user
        cursor.execute('DELETE FROM user WHERE user_id = %s', (agro[6],))
        connection.commit()

        flash('Agronomist deleted successfully!', 'success') # msg add when successed 
        return redirect(url_for('admin_m_agro', agro=agro))  # redirect to agro list
    except Exception as e:
        connection.rollback()  # rollback changes if any error occurs
        flash('Failed to delete agro!', 'error')
        return redirect(request.referrer)

@app.route('/reset_password/<int:agro_id>', methods=['POST'])
def reset_password(agro_id):
    cursor = getCursor()
    cursor.execute('SELECT agro.agro_id, agro.first_name, agro.last_name, agro.address, agro.phone_num, agro.date_joined, user.user_id, user.username, user.password, user.email, user.role, user.status FROM agro JOIN user ON agro.user_id = user.user_id WHERE agro.agro_id = %s', (agro_id,))
    agro = cursor.fetchone()

    try:
        # set initial_password
        initial_password = 'password123'

        # hash initial_password
        hashed_password = hashing.hash_value(initial_password, salt='8010')

        # get id that relative to agro
        user_id = agro[6]

        # update password
        cursor.execute('UPDATE user SET password = %s WHERE user_id = %s', (hashed_password, user_id))
        connection.commit()

        flash('Password reset successfully!', 'success')
    except Exception as e:
        connection.rollback()
        flash('Failed to reset password!', 'error')

    return redirect(url_for('admin_m_agro'))  # redirect to agro list

@app.route('/admin/manage_staff')
def admin_m_staff():
    if 'loggedin' in session:
        # login and fetch details
        cursor = getCursor()
        cursor.execute('SELECT * FROM staff_admin WHERE user_id = %s', (session['id'],))
        admin_info = cursor.fetchone()
        print("admin_info:", admin_info)

        # get agro info
        cursor.execute('''
            SELECT staff_admin.staff_id, staff_admin.first_name, staff_admin.last_name,
            staff_admin.work_phone_num, staff_admin.hire_date, staff_admin.dept,
            user.username, user.email, user.role, user.status
            FROM staff_admin
            JOIN user ON staff_admin.user_id = user.user_id
        ''')
        combined_list = cursor.fetchall()
        print(combined_list)

    return render_template('5_admin_manage_staff.html', combined_list=combined_list, admin=admin_info)

@app.route('/admin/staff/update/<int:id>', methods=['GET', 'POST'])
def update_staff(id):
    cursor = getCursor()
    if request.method == 'POST':
        staff_id = request.form['staff_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        work_phone_num = request.form['work_phone_num']
        hire_date = request.form['hire_date']
        dept = request.form['dept']
        email = request.form['email']
        role = request.form['role']
        status = request.form['status']
        print("Form data:", request.form)

        # updated date
        cursor.execute('UPDATE staff_admin SET first_name=%s, last_name=%s, work_phone_num=%s, hire_date=%s, dept=%s WHERE staff_id=%s',
                       (first_name, last_name, work_phone_num, hire_date, dept, staff_id))
        print('UPDATE staff_admin SET first_name=%s, last_name=%s, work_phone_num=%s, hire_date=%s, dept=%s, WHERE staff_id=%s'
            % (first_name, last_name, work_phone_num, hire_date, dept, staff_id))
        cursor.execute('UPDATE user SET email=%s, role=%s, status=%s WHERE user_id=(SELECT user_id FROM staff_admin WHERE staff_id=%s)',
                        (email, role, status, staff_id))

        connection.commit()

        return redirect(url_for('admin_m_staff'))
    else:
        # get agro info
        cursor.execute('''
            SELECT staff_admin.staff_id, staff_admin.first_name, staff_admin.last_name,
            staff_admin.work_phone_num, staff_admin.hire_date, staff_admin.dept,
            user.username, user.email, user.role, user.status
            FROM staff_admin
            JOIN user ON staff_admin.user_id = user.user_id
            WHERE staff_admin.staff_id = %s
        ''', (id,))
        staff = cursor.fetchone()

        return render_template('5_admin_manage_staff_edit.html', staff=staff)

@app.route('/admin/profile', methods=['GET', 'POST'])
def admin_profile():
    # check if loggined
    if 'loggedin' in session:
        # login and fetch details
        cursor = getCursor()
        cursor.execute('SELECT * FROM staff_admin WHERE user_id = %s', (session['id'],))
        admin_info = cursor.fetchone()
        print("admin_info:", admin_info)

        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            phone_num = request.form['phone_num']
            email = request.form['email']
            current_password = request.form['currentPassword']
            new_password = request.form['newPassword']
            confirm_password = request.form['confirmPassword']
            print("Form Data - First Name:", first_name)
            print("Form Data - Last Name:", last_name)
            print("Form Data - Phone Number:", phone_num)
            print("Form Data - Email:", email)
            print("Form Data - Current Password:", current_password)
            print("Form Data - New Password:", new_password)
            print("Form Data - Confirm Password:", confirm_password)


            # verify password
            cursor.execute('SELECT password FROM user WHERE user_id = %s', (session['id'],))
            stored_password = cursor.fetchone()[0]
            if not hashing.check_value(stored_password, current_password, salt='8010'):
                # if password incorect
                return render_template('5_admin_profile.html', 
                                       msg='Current password is incorrect.', 
                                       msg_type='error',
                                       admin=admin_info)

            # check old password and new password
            if new_password and confirm_password:
                if new_password != confirm_password:
                    return render_template('5_admin_profile.html', 
                                           msg='New password and confirm password do not match.', 
                                           msg_type='error',
                                           admin=admin_info)
                hashed_new_password = hashing.hash_value(new_password, salt='8010')
                # update password
                cursor.execute('UPDATE user SET password=%s WHERE user_id=%s', (hashed_new_password, session['id']))


            # update other user information
            cursor.execute('UPDATE staff_admin SET first_name=%s, last_name=%s, address=%s, phone_num=%s WHERE user_id=%s',
                           (first_name, last_name, phone_num, session['id']))
            print('UPDATE staff_admin SET first_name=%s, last_name=%s, address=%s, phone_num=%s WHERE user_id=%s' % 
                  (first_name, last_name, phone_num, session['id']))
            cursor.execute('UPDATE user SET email=%s WHERE user_id=%s', (email, session['id']))
            print('UPDATE user SET email=%s WHERE user_id=%s' % (email, session['id']))
            print("Before commit")
            connection.commit()
            print("After commit")
            
            print("Updating user and staff table...")
            
            # updated in session
            session['email'] = email
            print("New email:", email)
            
            return render_template('5_admin_profile', 
                                   msg='Profile updated successfully.', 
                                   msg_type='success',
                                   admin=admin_info)

        return render_template('5_admin_profile.html', admin=admin_info)
    return redirect(url_for('login'))

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
        input_password = request.form['password'] 
        
        # Get user data from MySQL
        cursor = getCursor()
        cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
        user = cursor.fetchone()

        if user:
            stored_password = user[2]  # Extract the stored hashed password

            # Check if the hashed input password matches the stored hashed password
            if hashing.check_value(stored_password, input_password, salt='8010'):
                print("Password verification succeeded.")

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

@app.route('/weed_list')
def weed_list1():
    cursor = getCursor()
    cursor.execute('SELECT * FROM guide_info WHERE guide_id = %s', (guide_id,))
    guide_id = cursor.fetchone()
    print("admin_info:", guide_id)

    return render_template('9_weed_list-1.html')

@app.route('/pest_list')
def pest_list1():
    cursor = getCursor()
    cursor.execute("SELECT * FROM guide_info")
    pest_guide = cursor.fetchall()
    print("admin_info:", pest_guide)

    return render_template('10_pest_list-1.html', pest=pest_guide)

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.clear()
    # Redirect to login page
    return redirect(url_for('login'))