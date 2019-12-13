from app import app
from flask import render_template, send_file, redirect, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from class_info import *
from AnalysisData.Class import class_type, class_highest_ranking, \
    class_best_subject, class_worse_subject, class_grade_distributed
from User.UserModel import User


@app.route('/')
def hello_world():
    if current_user.is_anonymous:
        return redirect(url_for('choose_identity'))
    else:
        if current_user.type == 'student':
            return redirect('/student_info/{}'.format(current_user.username))
        if current_user.type == 'teacher':
            return 'teacher page'


@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('hello_world'))
    if not request.args:
        return render_template('login.html')
    else:
        user = User.query.filter_by(username=request.args.get('username')).first()
        if user is None or not user.check_password(request.args.get('password')):
            return redirect(url_for('login'))
        else:
            login_user(user, remember=True)
            return redirect(url_for('hello_world'))


@app.route('/logout')
def logout():
    logout_user()
    return 'Bye'


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
    distributed_data = class_grade_distributed(class_index)[1]
    top_level = '较多' if distributed_data['A+'] > 5 else '处于平均水平'
    analysis = '该班成绩主要集中在{level}水平<br>顶尖同学数量{top_level}'.format(
        level=max(distributed_data, key=distributed_data.get), top_level=top_level)

    return render_template('class_info.html',
                           theme='vintage',
                           class_infos=class_infos,
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
             'test_time': grade.test.test_time,
             'grade_id': grade.ID,
             })
    for key, value in grades.items():
        first_index = min([v['index'] for v in value])
        for v in value:
            if v['index'] == first_index:
                v['is_show'] = True

    return render_template('student_info.html',
                           theme='vintage',
                           infos=[
                               {'key': 'Name', 'value': student.student_name},
                               {'key': 'ClassIndex', 'value': student.class_index}
                           ],
                           semesters=grades,
                           )


@app.route('/student_info/<string:student_name>')
def student_info_redirect(student_name: str):
    student_id = db.session.query(Student.ID).filter_by(student_name=student_name).first()[0]
    return redirect('/student_info/{}'.format(student_id))


@app.route('/test_info/<int:test_time>')
def test_info(test_time):
    test_data = {}
    test = Test.query.filter_by(test_time=test_time).first()
    test_data['name'] = test.test_name
    test_data['test_time'] = test.test_time
    return render_template('test_info.html'
                           , test=test_data,
                           theme='vintage')


@app.route('/search')
def search():
    return render_template('search.html')


# 路径问题，暂时启用
# @app.route('/favicon.ico')
# def favicon():
#     return send_file('../static/favicon.ico')


@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template('error.html',
                           error_code=404)


@app.errorhandler(500)
def service_error(e):
    print(e)
    return render_template('error.html',
                           error_code=500)
