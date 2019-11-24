from app import app
from app.models import *
import json
import Subject
import GradeRanking


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
