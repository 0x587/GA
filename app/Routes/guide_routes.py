from flask import render_template, abort
from app.Routes.api_routers import *


@app.route('/choose_Identity')
def choose_identity():
    return render_template('choose_identity.html')


@app.route('/choose_Identity/<string:user_identity>')
def identity(user_identity: str):
    if user_identity == 'student':
        return render_template('guide/student_select.html')
    elif user_identity == 'teacher':
        return render_template('guide/teacher_select.html')
    else:
        abort(404)
