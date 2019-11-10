from pyecharts.charts import Funnel, Timeline, Bar
from pyecharts import options as opts
from app.models import *
from pyecharts.globals import ThemeType


def class_grade_distributed(class_index: int) -> (Funnel, dict):
    students: list = Student.query.filter_by(class_index=class_index)
    data = {'top': 0, 'high': 0, 'medium': 0, 'low': 0, }
    for student in students:
        data[student.analysis[0].get_level()] += 1
    chart = (
        Funnel(init_opts=opts.InitOpts(width='100%', height='400px', theme=ThemeType.VINTAGE))
            .add('level', [list(z) for z in zip(data.keys(), data.values())],
                 sort_="none", gap=5, label_opts=opts.LabelOpts())
    )
    return chart, data


def class_type(class_index: int) -> str:
    if class_index in [1809, 1810]:
        return 'Experiment class'
    else:
        return 'Ordinary class'


def class_history_grade(class_index: int) -> Timeline:
    tl = Timeline(init_opts=opts.InitOpts(theme=ThemeType.VINTAGE))
    for test in Test.query.all():
        cag: ClassAverageGrade = ClassAverageGrade.query.filter(
            ClassAverageGrade.test_time == test.test_time,
            ClassAverageGrade.class_index == class_index,
        ).first()
        grades = [cag.chinese, cag.match, cag.english,
                  cag.physics, cag.chemistry, cag.biology, ]
        rankings = [cag.chinese_ranking, cag.match_ranking, cag.english_ranking,
                    cag.physics_ranking, cag.chemistry_ranking, cag.biology_ranking, ]
        bar = (
            Bar(init_opts=opts.InitOpts(theme=ThemeType.VINTAGE))
                .add_xaxis(['语文', '数学', '英语', '物理', '化学', '生物'])
                .add_yaxis('Grade', grades)
                .add_yaxis('Ranking', rankings)
                .set_global_opts(title_opts=opts.TitleOpts(test.test_name))
        )
        tl.add(bar, test.test_time)
    return tl
