from pyecharts.charts import Line, Bar, Radar
from pyecharts import options as opts
from app.models import *
from pyecharts.globals import ThemeType
import Subject
import GradeRanking


def student_grade_compared(student_grade: StudentGrade) -> Bar:
    """
    Uniapp专属
    生成该考生本次考试的成绩对比条形图。
    :param student_grade:本次考试成绩StudentGrade对象
    :return: bar:Bar对象
    """
    data = {'student_grade': [], 'average_grade': [], 'high_grade': []}
    subjects = Subject.subjects_by_grade(student_grade)
    for subject in subjects:
        data['student_grade'].append(student_grade.grade_dict()[subject])
        data['average_grade'].append(TestAverageGrade.query.filter_by(
            subject='理科', test_time=student_grade.test_time).first()
                                     .grade_dict()[subject])
        data['high_grade'].append(TestHighGrade.query.filter_by(
            subject='理科', test_time=student_grade.test_time).first()
                                  .grade_dict()[subject])

    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.VINTAGE))
            .add_xaxis(subjects)
            .add_yaxis('student_grade', data['student_grade'])
            .add_yaxis('average_grade', data['average_grade'])
            .add_yaxis('high_grade', data['high_grade'])
            .set_global_opts(
            title_opts=opts.TitleOpts('成绩对比图'),
            datazoom_opts=[
                opts.DataZoomOpts(
                    type_='inside',
                    range_start=0,
                    range_end=25,
                ),
                opts.DataZoomOpts(
                    type_='slider'
                )
            ]
        )
    )
    return bar


def student_grade_radar(student_grade: StudentGrade) -> Radar:
    """
    Uniapp专属
    生成该考生本次考试的排名雷达图。
    :param student_grade: 本次考试成绩StudentGrade对象
    :return: radar: Radar图表
    """
    subjects = Subject.subjects_by_grade(student_grade)
    data = {'student_ranking': [], 'average_ranking': [], 'high_ranking': []}
    for subject in subjects:
        data['student_ranking'].append(
            GradeRanking.grade2ranking(
                student_grade.test,
                student_grade.grade_dict()[subject], subject, student_grade.subject))
        data['average_ranking'].append(TestAverageGrade.query.filter_by(
            subject='理科', test_time=student_grade.test_time).first()
                                       .__dict__[subject + '_ranking'])
        data['high_ranking'].append(TestHighGrade.query.filter_by(
            subject='理科', test_time=student_grade.test_time).first()
                                    .__dict__[subject + '_ranking'])
    radar = (
        Radar(init_opts=opts.InitOpts())
            .add_schema(
            schema=[
                opts.RadarIndicatorItem(
                    name=Subject.en2cn(subject),
                    color='#FFF',
                    max_=max(
                        data['student_ranking'] + data['average_ranking'] + data['high_ranking']) + 50
                ) for subject in subjects
            ],
            textstyle_opts=opts.TextStyleOpts(font_size=18)
        )
            .set_global_opts(
            legend_opts=opts.LegendOpts(
                textstyle_opts=opts.TextStyleOpts(
                    color='#FFF',
                    font_size=14,
                )
            )
        )
            .set_series_opts()
            .add('我的排名', [data['student_ranking']], color='#e098c7',
                 linestyle_opts=opts.LineStyleOpts(width=2.5),
                 label_opts=opts.LabelOpts(is_show=True, font_size=13),
                 tooltip_opts=opts.TooltipOpts(is_show=False))
            .add('平均排名', [data['average_ranking']], color='#8fd3e8',
                 linestyle_opts=opts.LineStyleOpts(width=2.5),
                 label_opts=opts.LabelOpts(is_show=True, font_size=13),
                 tooltip_opts=opts.TooltipOpts(is_show=False))
            .add('重点线排名', [data['high_ranking']], color='#cc70af',
                 linestyle_opts=opts.LineStyleOpts(width=2.5),
                 label_opts=opts.LabelOpts(is_show=True, font_size=13),
                 tooltip_opts=opts.TooltipOpts(is_show=False))
    )
    return radar
