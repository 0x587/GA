from flask import request
from UniApp.uniapp import uniapp
from app.models import StudentGrade
import json
import Subject


@uniapp.route('/grade/<int:grade_id>')
def grade_query(grade_id: int):
    result = {'code': 200, 'msg': 'Request succeeded', 'data': {}}
    grade = StudentGrade.query.filter_by(ID=grade_id).first()
    includes = []
    if request.args.get('includes'):
        includes = request.args.get('includes').split(',')
    if not grade:
        result['code'] = 404
        result['msg'] = 'This GradeID does not exist'
    else:
        result['data']['grade'] = {}
        if 'ranking' in includes:
            result['data']['ranking'] = {}
        for subject in Subject.li_all_subject():
            result['data']['grade'][subject] = grade.__dict__[subject]
            if 'ranking' in includes:
                result['data']['ranking'][subject] = grade.__dict__[subject + '_ranking']
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
