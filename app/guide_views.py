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

@app.route('/pest_list')
def pest_list():
    cursor = getCursor()
    cursor.execute("""
        SELECT guide_info.guide_id, guide_info.common_name, guide_info.name, guide_info.common_name, image.image_path 
        FROM guide_info guide_info
        INNER JOIN image image ON guide_info.guide_id = image.guide_id 
        WHERE guide_info.item_type = 'pest'
    """)
    pest_list = cursor.fetchall()
    cursor.close()
    return render_template('3_agro_pest.html', pest_list=pest_list)

@app.route('/weed_list')
def weed_list():
    cursor = getCursor()
    cursor.execute("""
        SELECT guide_info.guide_id, guide_info.name, guide_info.common_name, image.image_path 
        FROM guide_info guide_info
        INNER JOIN image image ON guide_info.guide_id = image.guide_id 
        WHERE guide_info.item_type = 'weed'
    """)
    weed_list = cursor.fetchall()
    cursor.close()
    return render_template('3_agro_weed.html', weed_list=weed_list)

@app.route('/info/<item_type>/<int:guide_id>')
def guide_info(item_type, guide_id):
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
        if item_type == 'pest':
            return render_template('3_agro_pest_details.html', item_info=item_info, is_primary=item_info[10])
        elif item_type == 'weed':
            return render_template('3_agro_weed_details.html', item_info=item_info, is_primary=item_info[10])
    return render_template('404.html')



