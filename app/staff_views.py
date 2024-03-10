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


def get_staff_info(user_id):
    cursor = getCursor()
    cursor.execute('SELECT * FROM staff_admin WHERE user_id = %s', (user_id,))
    staff_info = cursor.fetchone()
    cursor.close()
    return staff_info

@app.route('/staff/home')
def staff_home():
    if 'loggedin' in session:
        # login and fetch details
        staff_info = get_staff_info(session['id'])
        return render_template('4_staff_home.html', staff_info=staff_info)
    else:
        # return a message if not logged in
        return "You are not logged in. Please log in to access this page."

@app.route('/staff/view_guide')
def staff_view_guide():
    if 'loggedin' in session:
        staff_info = get_staff_info(session['id'])
        cursor = getCursor()
        # fetch weed guides
        cursor.execute("SELECT * FROM guide_info WHERE item_type = 'weed'")
        weed_guides = cursor.fetchall()
        
        # fetch pest guides
        cursor.execute("SELECT * FROM guide_info WHERE item_type = 'pest'")
        pest_guides = cursor.fetchall()
        
        cursor.close()
        
        return render_template('4_staff_view_guide.html', weed_guides=weed_guides, pest_guides=pest_guides, staff_info=staff_info)
    else:
        return "You are not logged in. Please log in to access this page."

# define upload file
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app', 'static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

@app.route('/admin/delete/<int:guide_id>', methods=['POST'])
def delete_guide(guide_id):
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
    return redirect(url_for('admin_view_guides', guide=guide, msg=msg))

@app.route('/admin/edit/<int:guide_id>', methods=['GET', 'POST'])
def admin_edit_guide(guide_id):
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

            return redirect(url_for('admin_edit_guide', guide_id=guide_id))

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

    return render_template('5_admin_view_edit.html', guide=guide, msg=msg, is_primary=guide[10])

@app.route('/staff/<item_type>/<int:guide_id>')
def staff_view_guides_list(guide_id, item_type):
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
        return render_template('4_staff_view_guide_list.html', item_info=item_info, is_primary=item_info[10])
    else:
        return render_template('404.html')
    
@app.route('/staff/add_new', methods=['GET', 'POST'])
def staff_add_new():
    msg = '' 
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
        is_primary = request.form.get('is_primary') == 'on'  # Convert checkbox value to boolean
        image_data = request.files['image_data']
        print("Form data:", request.form)

        cursor = getCursor()

        # Check if the species already exists
        cursor.execute('SELECT COUNT(*) FROM guide_info WHERE name = %s OR common_name = %s', (name, common_name))
        existing_species_count = cursor.fetchone()[0]
        if existing_species_count > 0:
            # Species already exists
            msg = 'Species already exists.'

        else:
            # Handle image upload
            if image_data:
                # Check image size
                if len(image_data.read()) > 64 * 1024:  # Convert KB to bytes
                    msg = 'Please upload an image smaller than 64KB.'
                else:
                    # Reset file pointer after reading
                    image_data.seek(0)

                    # Read image data
                    image_data = image_data.read()

                    # Store image data as blob in MySQL
                    cursor.execute('INSERT INTO image (is_primary, image_data) VALUES (%s, %s)', (is_primary, image_data))
                    # Get the last inserted image_id
                    image_id = cursor.lastrowid

                    # Insert other data along with the image
                    cursor.execute('INSERT INTO guide_info (item_type, name, common_name, key_char, bio, impact, control, further_info, image_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (item_type, name, common_name, key_char, bio, impact, control, further_info, image_id))
                    guide_id = cursor.lastrowid

                    # Update guide_id in the image table
                    cursor.execute('UPDATE image SET guide_id = %s WHERE image_id = %s', (guide_id, image_id))
                    # Update other fields in the guide_info table
                    cursor.execute('UPDATE guide_info SET item_type = %s, name = %s, common_name = %s, key_char = %s, bio = %s, impact = %s, control = %s, further_info = %s WHERE guide_id = %s', (item_type, name, common_name, key_char, bio, impact, control, further_info, guide_id))
                    connection.commit()

                    # Success flash message
                    flash('Species added successfully!', 'success')
    
    return render_template('4_staff_view_add.html', msg=msg)

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
    connection = getConnection()
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
            cursor.execute('UPDATE staff_admin SET first_name=%s, last_name=%s, work_phone_num=%s WHERE user_id=%s',
                           (first_name, last_name, phone_num, session['id']))
            print('UPDATE staff_admin SET first_name=%s, last_name=%s, work_phone_num=%s WHERE user_id=%s' % 
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