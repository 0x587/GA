from pyecharts.charts import Funnel
from pyecharts import options as opts
from app.models import *


def class_grade_distributed(class_index: int) -> Funnel:
    students: list = Student.query.filter_by(class_index=class_index)
    data = {'top': 0, 'high': 0, 'medium': 0, 'low': 0, }
    for student in students:
        data[student.analysis[0].get_level()] += 1
    chart = (
        Funnel(init_opts=opts.InitOpts(width='100%', height='400px'))
            .add('level', [list(z) for z in zip(data.keys(), data.values())],
                 sort_="none", gap=5, label_opts=opts.LabelOpts())
    )
    return chart


def class_type(class_index: int) -> str:
    if class_index in [1809, 1810]:
        return 'Experiment class'
    else:
        return 'Ordinary class'
