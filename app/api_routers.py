from app import app
from app.models import *
from AnalysisData.Test import test_grade_distributed

import json
import Subject
import GradeRanking
import numpy as np


@app.route('/api/student/grade/analysis/<int:grade_id>')
def student_grade_analysis_table_data(grade_id: int):
    result = {'code': 0, 'msg': '', 'data': [{} for _ in range(7)]}

    grade = StudentGrade.query.filter_by(ID=grade_id).first()

    test_avg_grade = TestAverageGrade.query.filter_by(
        test_time=grade.test_time, subject='理科').first()

    test_high_grade = TestHighGrade.query.filter_by(
        test_time=grade.test_time, subject='理科').first()

    class_grade = ClassAverageGrade.query.filter_by(
        test_time=grade.test_time,
        class_index=grade.class_index,
    ).first()

    for subject in Subject.li_all_subject():
        result['data'][0][subject] = grade.grade_dict()[subject]
        result['data'][1][subject] = class_grade.grade_dict()[subject]
        result['data'][2][subject] = GradeRanking.grade2ranking_for_class(grade_id, subject)
        result['data'][3][subject] = test_avg_grade.grade_dict()[subject]
        result['data'][4][subject] = GradeRanking.grade2ranking_with_grade(grade_id, subject)
        result['data'][5][subject] = 'To be developed'
        result['data'][6][subject] = test_high_grade.grade_dict()[subject]

    result['data'][0]['key'] = '分数'
    result['data'][1]['key'] = '班级平均分'
    result['data'][2]['key'] = '班级名次'
    result['data'][3]['key'] = '年级平均分'
    result['data'][4]['key'] = '年级名次'
    result['data'][5]['key'] = '进退步'
    result['data'][6]['key'] = '重点线'
    return json.dumps(result)


@app.route('/api/test/data/total/<int:test_time>')
def test_total_table_data(test_time: int):
    test = Test.query.filter_by(test_time=test_time).first()
    grades = StudentGrade.query.filter_by(test_time=test_time, subject='理科').all()
    result = {'code': 0, 'msg': '', 'data': [{} for _ in range(11)]}

    test_avg_grade = TestAverageGrade.query.filter_by(
        test_time=test_time, subject='理科').first()

    for subject in Subject.li_all_subject():
        scores = [grade.grade_dict()[subject] for grade in grades]
        result['data'][0][subject] = Subject.subject_full_grade(subject)
        result['data'][1][subject] = len(test.student_grades)
        result['data'][2][subject] = test_avg_grade.grade_dict()[subject]
        result['data'][3][subject] = 'To be developed'
        result['data'][4][subject] = 'To be developed'
        result['data'][5][subject] = np.max(scores)
        result['data'][6][subject] = np.min(scores)
        result['data'][7][subject] = np.std(scores).round(1)
        result['data'][8][subject] = '{}%'.format((GradeRanking.grade_rate(
            scores, Subject.subject_full_grade(subject) * 0.9) * 100).__round__(1))
        result['data'][9][subject] = '{}%'.format((GradeRanking.grade_rate(
            scores, Subject.subject_full_grade(subject) * 0.8) * 100).__round__(1))
        result['data'][10][subject] = '{}%'.format((GradeRanking.grade_rate(
            scores, Subject.subject_full_grade(subject) * 0.6) * 100).__round__(1))

    result['data'][0]['key'] = '卷面分'
    result['data'][1]['key'] = '参考人数'
    result['data'][2]['key'] = '年级平均分'
    result['data'][3]['key'] = '普通班平均分'
    result['data'][4]['key'] = '实验班平均分'
    result['data'][5]['key'] = '最高分'
    result['data'][6]['key'] = '最低分'
    result['data'][7]['key'] = '标准差'
    result['data'][8]['key'] = '优秀率'
    result['data'][9]['key'] = '良好率'
    result['data'][10]['key'] = '及格率'
    return json.dumps(result)


@app.route('/api/test/data/distributed/<int:test_time>')
def test_distributed_table_data(test_time: int):
    result = test_grade_distributed(test_time)
    return json.dumps(result)
