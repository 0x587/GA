from pyecharts.charts import Bar
from pyecharts import options as opts
from app.models import *
from pyecharts.globals import ThemeType
import Subject


def test_grade_distributed(test_time: int) -> list:
    grades = StudentGrade.query.filter_by(test_time=test_time, subject='理科').all()
    result = [{} for _ in range(15)]

    for subject in Subject.li_all_subject(False):
        scores = [grade.grade_dict()[subject] for grade in grades]
        for i in range(15):
            result[14 - i][subject] = len([_ for _ in scores if i * 10 < _ < i * 10 + 10])

    for i in range(15):
        result[14 - i]['key'] = '{}分—{}分段'.format(i * 10, i * 10 + 10)
    return result


def test_grade_distributed_chart(test_time: int, subject: str = 'total') -> Bar:
    if subject != 'total':
        data = test_grade_distributed(test_time)
    else:
        totals = [_[0] for _ in db.session.query(StudentGrade.total).filter_by(
            test_time=test_time, subject='理科').all()]
        data = [{} for _ in range(50)]
        for i in range(50):
            data[49 - i]['key'] = '{}分-{}分段'.format(i * 15, i * 15 + 15)
            data[49 - i]['total'] = len([_ for _ in totals if i * 15 < _ < i * 15 + 15])
    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.VINTAGE))
            .add_yaxis('人数', [_[subject] for _ in data])
            .add_xaxis([d['key'] for d in data])
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(
                    rotate=-15
                )
            ),
            datazoom_opts=[opts.DataZoomOpts(type_='slider',
                                             range_start=5, range_end=55),
                           opts.DataZoomOpts(type_="inside")],
            legend_opts=opts.LegendOpts(is_show=False)
        )
    )
    return bar

