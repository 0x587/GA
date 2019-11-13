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


def class_subject(class_index: int) -> str:
    if class_index in [1818, 1819, 1820]:
        return '文科'
    else:
        return '理科'


def class_history_grade(class_index: int) -> Timeline:
    if class_subject(class_index) == '理科':
        ranking_max = 16
    else:
        ranking_max = 3
    # TODO  文科班主科分开排序
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
        grade_bar = (
            Bar(init_opts=opts.InitOpts(theme=ThemeType.VINTAGE))
                .add_xaxis(['语文', '数学', '英语', '物理', '化学', '生物'])
                .add_yaxis('Grade', grades)
                .extend_axis(
                yaxis=opts.AxisOpts(
                    axislabel_opts=opts.LabelOpts(formatter="{value} 名"),
                    min_=0, max_=ranking_max, interval=2,
                    is_inverse=True,
                )
            )
                .set_global_opts(
                title_opts=opts.TitleOpts(title=test.test_name),
                yaxis_opts=opts.AxisOpts(
                    axislabel_opts=opts.LabelOpts(formatter="{value} 分"),
                ),
            )
        )
        ranking_bar = (
            Bar(init_opts=opts.InitOpts(theme=ThemeType.VINTAGE))
                .add_xaxis(['语文', '数学', '英语', '物理', '化学', '生物'])
                .add_yaxis('Ranking', rankings, yaxis_index=1)
                .set_global_opts(title_opts=opts.TitleOpts(test.test_name))
                .set_global_opts(yaxis_opts=opts.AxisOpts(is_inverse=True))

        )
        grade_bar.overlap(ranking_bar)
        tl.add(grade_bar, test.test_time)
    return tl


def class_highest_ranking(class_index: int):
    average_grade = ClassAverageGrade.query.filter_by(class_index=class_index).all()
    data = {g.test_time: g.total_ranking for g in average_grade}
    best_grade_time = min(data, key=data.get)
    return best_grade_time, data[best_grade_time]


def class_best_subject(class_index: int) -> list:
    average_grades = ClassAverageGrade.query.filter_by(class_index=class_index).all()
    subject_list = [g.limit_subject('best') for g in average_grades]
    return max(subject_list, key=subject_list.count)


def class_worse_subject(class_index: int) -> list:
    average_grades = ClassAverageGrade.query.filter_by(class_index=class_index).all()
    subject_list = [g.limit_subject('worse') for g in average_grades]
    return max(subject_list, key=subject_list.count)
