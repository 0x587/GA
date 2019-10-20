from app import app
from flask import render_template, request
from class_info import *


@app.route('/')
def hello_world():
    return render_template('welcome.html')


@app.route('/class_info/<int:class_index>')
def class_info(class_index):
    return render_template('class_info.html',
                           class_index=class_index,
                           student_count=student_count(class_index),
                           update_time=newest_data(), )
