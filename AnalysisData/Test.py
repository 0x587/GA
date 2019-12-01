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
            yaxis_opts=opts.AxisOpts(
                name='人数',
                axislabel_opts=opts.LabelOpts(
                    formatter='{value}人'
                )
            ),
            datazoom_opts=[opts.DataZoomOpts(type_='slider',
                                             range_start=5, range_end=55),
                           opts.DataZoomOpts(type_="inside")],
            legend_opts=opts.LegendOpts(is_show=False),
            title_opts=opts.TitleOpts(title='{}分数段分数'.format(subject), pos_left='47.5%')
        )
    )
    return bar


def test_avg_grade_compare(test_time: int) -> dict:
    """
    :param test_time:
    :return: charts:{subject:chart,,,} example:{'english':chart1,'chinese':chart2,,,}
    """
    result = {}
    avg_grades = ClassAverageGrade.query.filter_by(
        test_time=test_time, subject='理科').order_by(ClassAverageGrade.class_index).all()
    test_avg_grade = TestAverageGrade.query.filter_by(test_time=test_time, subject='理科').first()
    for subject in Subject.li_all_subject():
        avg = test_avg_grade.grade_dict()[subject]
        chart = (
            Bar(init_opts=opts.InitOpts(theme=ThemeType.VINTAGE))
                .add_xaxis(['{}班'.format(i + 1) for i in range(17)])
                .add_yaxis('平均分', [round(ag.grade_dict()[subject], 1)
                                   for ag in avg_grades], yaxis_index=0)
                .add_yaxis('平均分差', [round(ag.grade_dict()[subject] - avg, 1)
                                    for ag in avg_grades], yaxis_index=1,
                           )
                .set_global_opts(
                yaxis_opts=opts.AxisOpts(
                    name='均分',
                    axislabel_opts=opts.LabelOpts(
                        formatter='{value}分'
                    )
                ),
                xaxis_opts=opts.AxisOpts(
                    axisline_opts=opts.AxisLineOpts(
                        on_zero_axis_index=1
                    )
                ),
                datazoom_opts=[
                    opts.DataZoomOpts(type_='slider', range_start=5, range_end=55),
                    opts.DataZoomOpts(type_='inside')
                ],
                title_opts=opts.TitleOpts(title='各班{}均分对比图'.format(subject))

            )
                .extend_axis(
                yaxis=opts.AxisOpts(
                    name='均分差',
                    axislabel_opts=opts.LabelOpts(
                        formatter='{value}分'
                    )
                )
            )
        )
        result[subject] = chart
    return result


def test_student_distributed(test_time: int) -> Bar:
    grades = StudentGrade.query.filter_by(test_time=test_time, subject='理科').all()
    count_student = len(grades)
    data = {'C': [], 'C+': [], 'B': [], 'B+': [], 'A': [], 'A+': []}
    for i in range(1801, 1818):
        for key, value in data.items():
            value.append(None)
        work_grades = [g for g in grades if g.class_index == i]
        for grade in work_grades:
            if data[grade.get_this_level(count_student)][i - 1801] is None:
                data[grade.get_this_level(count_student)][i - 1801] = 1
            else:
                data[grade.get_this_level(count_student)][i - 1801] += 1
    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.VINTAGE))
            .add_xaxis(['{}班'.format(i + 1) for i in range(17)])
            .set_global_opts(
            datazoom_opts=[
                opts.DataZoomOpts(type_='slider', range_start=5, range_end=75),
                opts.DataZoomOpts(type_='inside')
            ],
            yaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(
                    formatter='{value}人'
                )
            ),
            title_opts=opts.TitleOpts(
                title='学生构成分析'
            )
        )
    )
    for key, value in data.items():
        bar.add_yaxis(key, value, stack="stack1")
    bar.set_series_opts(
        label_opts=opts.LabelOpts(
            position='inside'
        )
    )
    return bar
