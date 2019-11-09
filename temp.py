from pyecharts.charts import Line, Funnel
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from app.models import *


# TODO 参数传递
def personal_history_grade(student: Student) -> Line:
    s = student
    key = [t.test_name for t in Test.query.all()]
    values = [g.total_ranking for g in s.grades]
    current_data: list = values.copy()
    current_data[-1] = None
    current_line = (Line(init_opts=opts.InitOpts(theme=ThemeType.WONDERLAND))
                    .add_xaxis(key)
                    .add_yaxis('A', current_data, is_smooth=True, is_connect_nones=True,
                               # label_opts=opts.LabelOpts(is_show=False),
                               markpoint_opts=opts.MarkPointOpts(
                                   data=[opts.MarkPointItem(symbol=r'image:///static/top.png',
                                                            symbol_size=60, type_='max'),
                                         opts.MarkPointItem(symbol=r'image:///static/low.png',
                                                            symbol_size=40, type_='min')]
                               )))
    future_data: list = [None for _ in range(len(values))]
    future_data[-2:] = values[-2:]
    future_line = (Line()
                   .add_xaxis(key)
                   .add_yaxis('A', future_data, is_smooth=True, is_connect_nones=True,
                              linestyle_opts=opts.LineStyleOpts(type_="dashed"),
                              markpoint_opts=opts.MarkPointOpts(
                                  data=[opts.MarkPointItem(
                                      symbol='circle',
                                      name="下次预测", coord=[key[-1], values[-1]], value=values[-1])]
                              ),
                              ))
    current_line.set_global_opts(title_opts=opts.TitleOpts(title='历次成绩',
                                                           subtitle='预测结果使用{}次方程拟合'.
                                                           format('二')))
    return current_line.overlap(future_line)


def class_grade_distributed(class_index: int) -> Funnel:
    students: list = Student.query.filter_by(class_index=class_index)
    data = {'top': 0, 'high': 0, 'medium': 0, 'low': 0, }
    for student in students:
        data[student.analysis[0].get_level()] += 1
    c = (
        Funnel()
            .add('level', [list(z) for z in zip(data.keys(), data.values())],
                 sort_="none", gap=5, label_opts=opts.LabelOpts())
            .set_global_opts(title_opts=opts.TitleOpts('level分布'))
    )
    return c
