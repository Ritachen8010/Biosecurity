# from flask import Flask
# from flask import render_template
# from flask import request
# from flask import redirect
# from flask import url_for
# from flask import session
# import re
# from datetime import datetime
# import mysql.connector
# from mysql.connector import FieldType
# import connect
# from flask_hashing import Hashing

# app = Flask(__name__)
# hashing = Hashing(app)
# app.secret_key = '8010'

# def hash_and_update_passwords():
#     connection = mysql.connector.connect(host='localhost', user='root', password='66722766', database='ladybug', port = "3306")
#     cursor = connection.cursor()
    
#     cursor.execute("SELECT user_id, password FROM user")
#     users = cursor.fetchall()

#     for user_id, password in users:
#         hashed_password = hashing.hash_value(password, salt='8010')
#         cursor.execute("UPDATE user SET password = %s WHERE user_id = %s", (hashed_password, user_id))
    
#     connection.commit()
#     cursor.close()
#     connection.close()

# if __name__ == "__main__":
#     hash_and_update_passwords()



