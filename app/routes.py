from app import app
from flask import render_template, request
from class_info import *
from AnalysisData.Class import class_grade_distributed, class_type, class_history_grade
from AnalysisData.Student import personal_history_grade


@app.route('/')
def hello_world():
    return render_template('welcome.html')


@app.route('/class_info/<int:class_index>')
def class_info(class_index):
    class_infos = {'class index': class_index,
                   'class type': class_type(class_index),
                   'count of student': student_count(class_index),
                   'last update time': newest_data_no_date(),
                   }
    student_infos = []
    for s in enumerate(Class.query.filter_by(index=class_index).first().students):
        details = ({'key': 'Grade level', 'value': s[1].analysis[0].get_level().title()},
                   {'key': 'Key', 'value': 'Value'})
        student_infos.append({'index': s[0], 'name': s[1], 'details': details,
                              'full_detail': None})
    return render_template('class_info.html',
                           history_chart=class_history_grade(class_index).render_embed(),
                           class_infos=class_infos,
                           distributed=class_grade_distributed(class_index).render_embed(),
                           students=student_infos, )
