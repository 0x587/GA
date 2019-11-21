from app import app
from flask import render_template, request
from class_info import *
from AnalysisData.Class import class_grade_distributed, class_type, \
    class_history_grade, class_highest_ranking, \
    class_best_subject, class_worse_subject
from AnalysisData.Student.base_chart import personal_history_grade, \
    student_grade_compared, student_grade_radar


@app.route('/')
def hello_world():
    return render_template('welcome.html')


@app.route('/class_info/<int:class_index>')
def class_info(class_index):
    best_time, best_ranking = class_highest_ranking(class_index)
    class_infos = {'class index': class_index,
                   'class type': class_type(class_index),
                   'count of student': student_count(class_index),
                   'last update time': newest_data_no_date(),
                   'historical highest ranking': best_ranking,
                   'historical best test': Test.query.filter_by(test_time=best_time).first().test_name,
                   'best subject': class_best_subject(class_index),
                   'worse subject': class_worse_subject(class_index),
                   }
    student_infos = []
    for s in enumerate(Class.query.filter_by(index=class_index).first().students):
        details = ({'key': 'Grade level', 'value': s[1].analysis[0].get_level().title()},
                   {'key': 'Key', 'value': 'Value'})
        student_infos.append({'index': s[0], 'name': s[1], 'details': details,
                              'full_detail': None, 'ID': s[1].ID})
    distributed_chart, distributed_data = class_grade_distributed(class_index)
    top_level = '较多' if distributed_data['top'] > 10 else '处于平均水平'
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
    grades = {}
    grade_result = StudentGrade.query.filter_by(student_ID=student_id).all()
    for index, grade in enumerate(grade_result):
        test_name = grade.test.test_name
        grades[test_name[:2] + test_name[-3:]] = []
    for index, grade in enumerate(grade_result):
        test_name = grade.test.test_name
        grades[test_name[:2] + test_name[-3:]].append(
            {'is_show': False,
             'index': index,
             'test_name': grade.test.test_name[2:4],
             'compared_chart': student_grade_compared(grade).render_embed(),
             'radar_chart': student_grade_radar(grade).render_embed()})
    for key, value in grades.items():
        first_index = min([v['index'] for v in value])
        for v in value:
            if v['index'] == first_index:
                v['is_show'] = True

    return render_template('student_info.html',
                           infos=[
                               {'key': 'Name', 'value': student.student_name},
                               {'key': 'ClassIndex', 'value': student.class_index}
                           ],
                           grades=[{'index': index,
                                    'data': a} for index, a in enumerate(grades.items())],
                           )
