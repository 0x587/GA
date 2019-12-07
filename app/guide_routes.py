from app import app
from flask import render_template, request
from app.api_routers import *


@app.route('/choose_Identity')
def choose_identity():
    return render_template('choose_identity.html')


@app.route('/choose_Identity/<string:user_identity>')
def identity(user_identity: str):
    if user_identity == 'student':
        return render_template('guide/student_select.html')
