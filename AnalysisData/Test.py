from pyecharts.charts import Bar
from pyecharts import options as opts
from app.models import *
from pyecharts.globals import ThemeType
import Subject


def test_grade_distributed(test_time: int) -> Bar:
    grades = StudentGrade.query.filter_by(test_time=test_time, subject='理科').all()
    result = {'code': 0, 'msg': '', 'data': [{} for _ in range(15)]}

    for subject in Subject.li_all_subject(False):
        scores = [grade.grade_dict()[subject] for grade in grades]
        for i in range(15):
            result['data'][14 - i][subject] = len([_ for _ in scores if i * 10 < _ < i * 10 + 10])

    for i in range(15):
        result['data'][14 - i]['key'] = '{}分—{}分段'.format(i * 10, i * 10 + 10)
    return result
