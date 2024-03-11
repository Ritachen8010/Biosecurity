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
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from flask import current_app
from flask import flash


# get personal details
def get_admin_info(user_id):
    cursor = getCursor()
    cursor.execute('SELECT * FROM staff_admin WHERE user_id = %s', (user_id,))
    admin_info = cursor.fetchone()
    cursor.close()
    return admin_info

@app.route('/admin/home')
def admin_home():
    # check if loggined
    if 'loggedin' in session:
        # fetch admin info if logged in
        admin_info = get_admin_info(session['id'])
        return render_template('5_admin_home.html', admin=admin_info)
    else:
        # return a message if not logged in
        return "You are not logged in. Please log in to access this page."

@app.route('/admin_view_guides')
def admin_view_guides():
    if 'loggedin' in session:
        admin_info = get_admin_info(session['id'])
        cursor = getCursor()
        # fetch weed guides
        cursor.execute("SELECT * FROM guide_info WHERE item_type = 'weed'")
        weed_guides = cursor.fetchall()
        
        # fetch pest guides
        cursor.execute("SELECT * FROM guide_info WHERE item_type = 'pest'")
        pest_guides = cursor.fetchall()
        
        cursor.close()
        
        return render_template('5_admin_view_guides.html', weed_guides=weed_guides, pest_guides=pest_guides, admin=admin_info)
    else:
        return "You are not logged in. Please log in to access this page."

@app.route('/admin/<item_type>/<int:guide_id>')
def admin_view_guides_list(guide_id, item_type):
    cursor = getCursor()
    cursor.execute("""
        SELECT guide_info.guide_id, guide_info.item_type, guide_info.name, guide_info.common_name, 
               guide_info.key_char, guide_info.bio, guide_info.impact, 
               guide_info.control, guide_info.further_info,
               image.image_path, image.is_primary
        FROM guide_info 
        INNER JOIN image ON guide_info.guide_id = image.guide_id 
        WHERE guide_info.guide_id = %s AND guide_info.item_type = %s
    """, (guide_id, item_type))
    item_info = cursor.fetchone()
    cursor.close()
    if item_info:
        return render_template('5_admin_view_guides_list.html', item_info=item_info, is_primary=item_info[10])
    else:
        return render_template('404.html')

# define upload file
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app', 'static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/admin/add_new', methods=['GET', 'POST'])
def admin_add_new():
    connection = getConnection()

    if request.method == 'POST':
        item_type = request.form['item_type']
        name = request.form['name']
        common_name = request.form['common_name']
        key_char = request.form['key_char']
        bio = request.form['bio']
        impact = request.form['impact']
        control = request.form['control']
        further_info = request.form['further_info']
        is_primary = request.form.get('is_primary') == 'on'

        cursor = getCursor()

        # Check if species already exists
        cursor.execute('SELECT COUNT(*) FROM guide_info WHERE name = %s OR common_name = %s', (name, common_name))
        existing_species_count = cursor.fetchone()[0]
        if existing_species_count > 0:
            return render_template('4_admin_add_new.html', 
                                   msg='Species already exists.', 
                                   msg_type='error')
        else:
            # Insert data into guide_info table
            cursor.execute('INSERT INTO guide_info (item_type, name, common_name, key_char, bio, impact, control, further_info) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (item_type, name, common_name, key_char, bio, impact, control, further_info))        
            connection.commit()
            guide_id = cursor.lastrowid

            # Handle image upload
            image_file = request.files.get('image')
            if image_file and image_file.filename:
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                secure_filename_ = secure_filename(image_file.filename)
                filename = f"{timestamp}_{secure_filename_}"
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                print("Save path:", save_path)  # Print save_path for debugging
                
                # Save the image
                image_file.save(save_path)
                
                # Insert image information into image table
                cursor.execute('INSERT INTO image (guide_id, image_path, is_primary) VALUES (%s, %s, %s)', (guide_id, filename, is_primary))
                connection.commit()
                image_id = cursor.lastrowid

                update_image_path(guide_id, filename, image_id)  # Update image path and ID
                
                # Success message
                return redirect(url_for('admin_view_guides'))
            else:
                return render_template('5_admin_view_add.html', 
                                   msg='Species already exists.', 
                                   msg_type='error')
            
# Update image path and ID
def update_image_path(guide_id, image_path, image_id):
    connection = getConnection()
    cursor = getCursor()

    # Update image path
    cursor.execute('''UPDATE image
                      SET image_path = %s
                      WHERE guide_id = %s AND image_id = %s''', 
                   (image_path, guide_id, image_id))
    
    connection.commit()
    connection.close()

@app.route('/staff/delete/<int:guide_id>', methods=['POST'])
def staff_delete_guide(guide_id):
    msg = ''
    # Get image ID
    image_id = request.form.get('image_id')

    # Get database connection and cursor
    connection = getConnection()
    cursor = getCursor()

    # Query guide information and image information to be deleted
    cursor.execute("""
        SELECT guide_info.guide_id, guide_info.item_type, guide_info.name, guide_info.common_name, 
               guide_info.key_char, guide_info.bio, guide_info.impact, 
               guide_info.control, guide_info.further_info,
               image.image_id, image.image_path, image.is_primary
        FROM guide_info 
        LEFT JOIN image ON guide_info.guide_id = image.guide_id 
        WHERE guide_info.guide_id = %s
        """, (guide_id,))
    guide = cursor.fetchone()

    try:
        # Delete from guide and photo
        cursor.execute("DELETE FROM image WHERE image_id = %s", (guide[9],))
        cursor.execute("DELETE FROM guide_info WHERE guide_id = %s", (guide_id,))
        connection.commit()

        flash('Guide and associated image deleted successfully.')
    except Exception as e:
        # Rollback transaction
        connection.rollback()
        flash('Failed to delete guide and associated image: ' + str(e))
    finally:
        # Close cursor and database connection
        cursor.close()
        connection.close()

    # Redirect to the guide list page
    return redirect(url_for('staff_view_guide', guide=guide, msg=msg))

@app.route('/staff/edit/<int:guide_id>', methods=['GET', 'POST'])
def staff_edit_guide(guide_id):
    msg = ''
    connection = getConnection()
    cursor = getCursor()

    if request.method == 'POST':
        item_type = request.form['item_type'] 
        name = request.form['name']
        common_name = request.form['common_name']
        key_char = request.form['key_char']
        bio = request.form['bio']
        impact = request.form['impact']
        control = request.form['control']
        further_info = request.form['further_info']
        is_primary = request.form.get('is_primary') == 'on'

        # upload photo
        image_file = request.files.get('image')
        if image_file and image_file.filename:
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            secure_filename_ = secure_filename(image_file.filename)
            filename = f"{timestamp}_{secure_filename_}"
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # save photo
            image_file.save(save_path)

            # update
            update_image_path(guide_id, filename, guide[11])

            # update for guide_info
            cursor.execute('''
                UPDATE guide_info 
                SET item_type = %s, name = %s, common_name = %s, key_char = %s, bio = %s, 
                    impact = %s, control = %s, further_info = %s 
                WHERE guide_id = %s
            ''', (item_type, name, common_name, key_char, bio, impact, control, further_info, guide_id))
            connection.commit()
            flash('Succeed.')

            return redirect(url_for('staff_edit_guide', guide_id=guide_id))

    # get guide info
    cursor.execute("""
        SELECT guide_info.guide_id, guide_info.item_type, guide_info.name, guide_info.common_name, 
        guide_info.key_char, guide_info.bio, guide_info.impact, 
        guide_info.control, guide_info.further_info,
        image.image_path, image.is_primary, image.image_id
        FROM guide_info 
        LEFT JOIN image ON guide_info.guide_id = image.guide_id 
        WHERE guide_info.guide_id = %s
    """, (guide_id,))
    guide = cursor.fetchone()

    return render_template('4_staff_view_edit.html', guide=guide, msg=msg, is_primary=guide[10])

@app.route('/admin/manage_agro', methods=['GET', 'POST'])
def admin_m_agro():
    if 'loggedin' in session:
        # fetch admin info if logged in
        admin_info = get_admin_info(session['id'])

        cursor = getCursor()
        # get agro info
        cursor.execute('''
            SELECT agro.agro_id, agro.first_name, agro.last_name, agro.address, 
            agro.phone_num, agro.date_joined, user.username, user.email, user.status
            FROM agro
            JOIN user ON agro.user_id = user.user_id
        ''')
        combined_list = cursor.fetchall()

        cursor.close() # close

        return render_template('5_admin_manage_agro.html', combined_list=combined_list, admin=admin_info)
    else:
        # return a message if not logged in
        return "You are not logged in. Please log in to access this page."

@app.route('/admin/agronomists/update/<int:id>', methods=['GET', 'POST'])
def update_agro(id):
    cursor = getCursor()
    connection = getConnection()
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

        flash('Updated successfully!', 'success')

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
    connection = getConnection()
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
        

        # Check if email already exists
        cursor = getCursor()
        cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
        existing_email = cursor.fetchone()
        if existing_email:
            msg = 'Email already exists!'
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
        user_id = cursor.lastrowid  # get new user_id

        # update agro.user id
        cursor.execute('UPDATE agro SET user_id = %s WHERE agro_id = %s', (user_id, agro_id))
        connection.commit()

        # success flash message
        flash('Agro added successfully!', 'success')

        cursor.close()

        return redirect(url_for('admin_m_agro'))
    else:
        return render_template('5_admin_manage_add_agro.html')
    
@app.route('/delete_agro/<int:agro_id>', methods=['POST'])
def delete_agro(agro_id):
    cursor = getCursor()
    connection = getConnection()
    cursor.execute('SELECT agro.agro_id, agro.first_name, agro.last_name, agro.address, agro.phone_num, agro.date_joined, user.user_id, user.username, user.password, user.email, user.role, user.status FROM agro JOIN user ON agro.user_id = user.user_id WHERE agro.agro_id = %s', (agro_id,))
    agro = cursor.fetchone()

    try:
        # delete from agro
        cursor.execute('DELETE FROM agro WHERE agro_id = %s', (agro_id,))
        # delete from user
        cursor.execute('DELETE FROM user WHERE user_id = %s', (agro[6],))
        connection.commit()


        flash('Agronomist deleted successfully!', 'success') # msg add when successed 

        cursor.close()

        return redirect(url_for('admin_m_agro', agro=agro))  # redirect to agro list
    except Exception as e:
        connection.rollback()  # rollback changes if any error occurs
        flash('Failed to delete agro!', 'error')
        return redirect(request.referrer)

@app.route('/reset_password/<int:agro_id>', methods=['POST'])
def reset_password(agro_id):
    cursor = getCursor()
    connection = getConnection()
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
        
        cursor.close()

    except Exception as e:
        connection.rollback()
        flash('Failed to reset password!', 'error')

    return redirect(url_for('admin_m_agro'))  # redirect to agro list

@app.route('/admin/manage_staff')
def admin_m_staff():
    if 'loggedin' in session:
        # fetch admin info if logged in
        admin_info = get_admin_info(session['id'])

        cursor = getCursor()

        # get staff info
        cursor.execute('''
            SELECT staff_admin.staff_id, staff_admin.first_name, staff_admin.last_name,
            staff_admin.work_phone_num, staff_admin.hire_date, staff_admin.dept,
            user.username, user.email, user.role, user.status
            FROM staff_admin
            JOIN user ON staff_admin.user_id = user.user_id
        ''')
        combined_list = cursor.fetchall()

        cursor.close()

        return render_template('5_admin_manage_staff.html', combined_list=combined_list, admin=admin_info)
    else:
        # return a message if not logged in
        return "You are not logged in. Please log in to access this page."

@app.route('/admin/staff/update/<int:id>', methods=['GET', 'POST'])
def update_staff(id):
    cursor = getCursor()
    connection = getConnection()
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

        flash('Updated successfully!', 'success')

        cursor.close()

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

@app.route('/add_staff', methods=['GET', 'POST'])
def add_staff():
    connection = getConnection()
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        work_phone_num = request.form['work_phone_num']
        hire_date = request.form['hire_date']
        dept = request.form['dept']
        username = request.form['username']
        password = request.form['password'] #raw password
        email = request.form['email']
        role = request.form['role']
        status = request.form['status']

        # Check if username already exists
        cursor = getCursor()
        cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            flash('Account already exists!', 'info')
            return render_template('5_admin_manage_add_staff.html')

        # Check if email already exists
        cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
        existing_email = cursor.fetchone()
        if existing_email:
            flash('Email already exists!')
            return render_template('5_admin_manage_add_staff.html')

        # hash with salt
        hashed_password = hashing.hash_value(password, salt='8010')

        # insert new staff
        cursor = getCursor()
        cursor.execute('INSERT INTO staff_admin (first_name, last_name, work_phone_num, hire_date, dept) VALUES (%s, %s, %s, %s, %s)',
               (first_name, last_name, work_phone_num, hire_date, dept))
        staff_id = cursor.lastrowid  # get new staff_id

        # insert new user
        cursor.execute('INSERT INTO user (username, password, email, role, status) VALUES (%s, %s, %s, %s, %s)',
               (username, hashed_password, email, role, status))
        user_id = cursor.lastrowid  # get new user_id

        # update staff_admin.user id
        cursor.execute('UPDATE staff_admin SET user_id = %s WHERE staff_id = %s', (user_id, staff_id))
        connection.commit()

        # success flash message
        flash('Agro added successfully!', 'success')

        cursor.close()

        return redirect(url_for('admin_m_staff'))
    else:
        return render_template('5_admin_manage_add_staff.html')

@app.route('/delete_staff/<int:staff_id>', methods=['POST'])
def delete_staff(staff_id):
    cursor = getCursor()
    connection = getConnection()
    cursor.execute('SELECT staff_admin.staff_id, staff_admin.first_name, staff_admin.last_name, staff_admin.work_phone_num, staff_admin.hire_date, staff_admin.dept, user.user_id, user.username, user.password, user.email, user.role, user.status FROM staff_admin JOIN user ON staff_admin.user_id = user.user_id WHERE staff_admin.staff_id = %s', (staff_id,))
    staff = cursor.fetchone()

    try:
        # delete from user
        cursor.execute('DELETE FROM user WHERE user_id = %s', (staff[6],))
        # delete from staff
        cursor.execute('DELETE FROM staff_admin WHERE staff_id = %s', (staff_id,))
        print("Deleting staff with ID:", staff_id)
        connection.commit()


        flash('Staff deleted successfully!', 'success') # msg add when successed 

        cursor.close()

        return redirect(url_for('admin_m_staff', staff=staff))  # redirect to staff list
    except Exception as e:
        connection.rollback()  # rollback changes if any error occurs
        flash('Failed to delete staff!', 'error')
        return redirect(request.referrer)

@app.route('/reset_password_staff/<int:staff_id>', methods=['POST'])
def reset_password_staff(staff_id):
    cursor = getCursor()
    connection = getConnection()
    cursor.execute('SELECT staff_admin.staff_id, staff_admin.first_name, staff_admin.last_name, staff_admin.work_phone_num, staff_admin.hire_date, staff_admin.dept, user.user_id, user.username, user.password, user.email, user.role, user.status FROM staff_admin JOIN user ON staff_admin.user_id = user.user_id WHERE staff_admin.staff_id = %s', (staff_id,))
    staff = cursor.fetchone()

    try:
        # set initial_password
        initial_password = 'password123'

        # hash initial_password
        hashed_password = hashing.hash_value(initial_password, salt='8010')

        # get id that relative to staff
        user_id = staff[6]

        # update password
        cursor.execute('UPDATE user SET password = %s WHERE user_id = %s', (hashed_password, user_id))
        connection.commit()

        flash('Password reset successfully!', 'success')
        
        cursor.close()

    except Exception as e:
        connection.rollback()
        flash('Failed to reset password!', 'error')

    return redirect(url_for('admin_m_staff'))  # redirect to staff list

@app.route('/admin/profile', methods=['GET', 'POST'])
def admin_profile():
    connection = getConnection()
    # check if loggined
    if 'loggedin' in session:
        # Fetch admin info if logged in
        admin_info = get_admin_info(session['id'])

        cursor = getCursor()

        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            phone_num = request.form['work_phone_num']
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
            cursor.execute('UPDATE staff_admin SET first_name=%s, last_name=%s, work_phone_num=%s WHERE user_id=%s',
                           (first_name, last_name, phone_num, session['id']))
            print('UPDATE staff_admin SET first_name=%s, last_name=%s, work_phone_num=%s WHERE user_id=%s' % 
                  (first_name, last_name, phone_num, session['id']))
            cursor.execute('UPDATE user SET email=%s WHERE user_id=%s', (email, session['id']))
            print('UPDATE user SET email=%s WHERE user_id=%s' % (email, session['id']))
            print("Before commit")
            connection.commit()
            print("After commit")
            
            # updated in session
            session['email'] = email
            print("New email:", email)
            
            return render_template('5_admin_profile.html', 
                                   msg='Profile updated successfully.', 
                                   msg_type='success',
                                   admin=admin_info)

        return render_template('5_admin_profile.html', admin=admin_info)
    else:
        # return a message if not logged in
        return redirect(url_for('login'))


