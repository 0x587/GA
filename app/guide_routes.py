from app import app
from flask import render_template, send_file
from app.api_routers import *


@app.route('/choose_Identity')
def choose_identity():
    return render_template('choose_identity.html')
