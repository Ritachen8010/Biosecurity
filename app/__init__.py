from flask import Flask
from flask_hashing import Hashing

app = Flask(__name__)
hashing = Hashing(app)
app.secret_key = '8010'

from app import public
from app import login_register_logout
from app import guide_views
from app import agro_views
from app import admin_views
from app import staff_views
