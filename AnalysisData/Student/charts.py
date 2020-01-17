from pyecharts.charts import Line, Bar, Radar
from pyecharts import options as opts
from app.models import *
from pyecharts.globals import ThemeType
import Subject
import GradeRanking


def personal_history_grade(student: Student) -> Line:
    """
    生成该考生历次成绩折线图。
    :param student:Student
    :return: line:Line
    """
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


def student_grade_compared(student_grade: StudentGrade) -> Bar:
    """
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
            .set_global_opts(title_opts=opts.TitleOpts('成绩对比图'))
    )
    return bar


def student_grade_radar(student_grade: StudentGrade) -> Radar:
    """
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
        Radar(init_opts=opts.InitOpts(bg_color='#fef8ef'))
            .add_schema(
            schema=[
                opts.RadarIndicatorItem(
                    name=subject,
                    color='#778899',
                    max_=max(
                        data['student_ranking'] + data['average_ranking'] + data['high_ranking']) + 50
                ) for subject in subjects
            ],
            textstyle_opts=opts.TextStyleOpts(font_size=18)
        )
            .set_global_opts(title_opts=opts.TitleOpts('名次雷达图'), )
            .set_series_opts()
            .add('student_ranking', [data['student_ranking']], color='#d7ab82',
                 linestyle_opts=opts.LineStyleOpts(width=2.5),
                 label_opts=opts.LabelOpts(is_show=True, font_size=14),
                 tooltip_opts=opts.TooltipOpts(is_show=False))
            .add('average_ranking', [data['average_ranking']], color='#919e8b',
                 linestyle_opts=opts.LineStyleOpts(width=2.5),
                 label_opts=opts.LabelOpts(is_show=True, font_size=14),
                 tooltip_opts=opts.TooltipOpts(is_show=False))
            .add('high_ranking', [data['high_ranking']], color='#d87c7c',
                 linestyle_opts=opts.LineStyleOpts(width=2.5),
                 label_opts=opts.LabelOpts(is_show=True, font_size=14),
                 tooltip_opts=opts.TooltipOpts(is_show=False))
    )
    return radar


def student_history_ranking(student_id: int) -> dict:
    result = {}
    result_chart = {}
    grades = StudentGrade.query.filter_by(
        student_ID=student_id, subject='理科').order_by(StudentGrade.test_time).all()
    test_names = [t.test_name for t in Test.query.order_by(Test.test_time).all()]
    print(test_names)
    for subject in Subject.li_all_subject():
        result[subject] = []
        for grade in grades:
            grade: StudentGrade
            result[subject].append(grade.__dict__[subject + '_ranking'])
    for subject in Subject.li_all_subject():
        line = (
            Line()
                .add_xaxis(test_names)
                .add_yaxis(
                '排名',
                result[subject],
                markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]), )
                .set_global_opts(
                title_opts=opts.TitleOpts(
                    title=Subject.en2cn(subject) + '科历次成绩走势',
                    subtitle='虚线为平均排名'
                ),
            )
        )
        result_chart[subject] = line
    return result_chart
