from pyecharts.charts import Line, Bar
from pyecharts import options as opts
from app.models import *
from pyecharts.globals import ThemeType
import Subject


def student_type(class_index: int) -> str:
    """
    返回学生类型。
    :param class_index:
    :return: student_type
    :rtype: str
    """
    if class_index in [1809, 1810]:
        return 'Experiment student'
    else:
        return 'Ordinary student'


def student_subject(class_index: int) -> str:
    """
    返回学生学科类型。
    :param class_index:
    :return: student_subject
    :rtype: str
    """
    if class_index in [1818, 1819, 1820]:
        return '文科'
    else:
        return '理科'


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
    :param student_grade:StudentGrade
    :return: bar:Bar
    """
    data = {'student_grade': [], 'average_grade': [], 'high_grade': []}
    if student_grade.subject == '文科':
        subjects = Subject.wen_all_subject(True)
    else:
        subjects = Subject.li_all_subject(True)
    for subject in subjects:
        data['student_grade'].append(student_grade.grade_dict()[subject])
        data['average_grade'].append(TestAverageGrade.query.filter_by(
            subject='理科', test_time=student_grade.test_time).first()
                                     .grade_dict()[subject])
        data['high_grade'].append(TestHighGrade.query.filter_by(
            subject='理科', test_time=student_grade.test_time).first()
                                  .grade_dict()[subject])

    bar = (
        Bar()
            .add_xaxis(subjects)
            .add_yaxis('student_grade', data['student_grade'])
            .add_yaxis('average_grade', data['average_grade'])
            .add_yaxis('high_grade', data['high_grade'])
    )
    return bar
