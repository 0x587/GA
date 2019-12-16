from UniApp.uniapp import uniapp
from app.models import StudentGrade
import json


@uniapp.route('/grade/<int:grade_id>')
def grade_query(grade_id: int):
    result = {'code': 200, 'msg': 'Request succeeded', 'data': {}}
    grade = StudentGrade.query.filter_by(ID=grade_id).first()
    grade: StudentGrade
    if not grade:
        result['code'] = 404
        result['msg'] = 'This GradeID does not exist'
    else:
        result['data']['grade'] = grade.grade_dict()
    return json.dumps(result)


@uniapp.errorhandler(500)
def server_error(error_code):
    result = {
        'code': str(error_code),
        'msg': 'This request triggered an internal server error.'
               ' Please check whether the request method or parameters are valid.',
        'data': None
    }
    return json.dumps(result), {'Content-Type': 'json'}
