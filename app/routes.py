from app import app
from flask import render_template, request
from class_info import *
from AnalysisData.Class import class_grade_distributed, class_type, \
    class_history_grade, historical_highest_ranking
from AnalysisData.Student import personal_history_grade


@app.route('/')
def hello_world():
    return render_template('welcome.html')


@app.route('/class_info/<int:class_index>')
def class_info(class_index):
    best_time, best_ranking = historical_highest_ranking(class_index)
    class_infos = {'class index': class_index,
                   'class type': class_type(class_index),
                   'count of student': student_count(class_index),
                   'last update time': newest_data_no_date(),
                   'historical highest ranking': best_ranking,
                   'historical best test': Test.query.filter_by(test_time=best_time).first().test_name,
                   'best subject': '',
                   }
    student_infos = []
    for s in enumerate(Class.query.filter_by(index=class_index).first().students):
        details = ({'key': 'Grade level', 'value': s[1].analysis[0].get_level().title()},
                   {'key': 'Key', 'value': 'Value'})
        student_infos.append({'index': s[0], 'name': s[1], 'details': details,
                              'full_detail': None, 'ID': s[1].ID})
    distributed_chart, distributed_data = class_grade_distributed(class_index)
    if distributed_data['top'] > 10:
        top_level = '较多'
    else:
        top_level = '处于平均水平'
    analysis = '该班成绩主要集中在{level}水平<br>顶尖同学数量{top_level}'.format(
        level=max(distributed_data, key=distributed_data.get), top_level=top_level)

    return render_template('class_info.html',
                           history_chart=class_history_grade(class_index).render_embed(),
                           class_infos=class_infos,
                           distributed=distributed_chart.render_embed(),
                           distributed_analysis=analysis,
                           students=student_infos, )


@app.route('/student_info/<int:student_id>')
def student_info(student_id):
    student = Student.query.filter_by(ID=student_id).first()
    return render_template('student_info.html',
                           infos=[
                               {'key': 'Name', 'value': student.student_name},
                               {'key': 'ClassIndex', 'value': student.class_index}
                           ])
