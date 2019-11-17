from app.models import *
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


def set_level():
    """
    计算所有学生的平均排名。
    :return: None
    """
    grades = Test.query.order_by(Test.test_time.desc()).first().grades
    liberal_arts_count = len([g for g in grades if g.subject == '文科'])
    science_count = len([g for g in grades if g.subject == '理科'])
    for student in Student.query.all():
        ranking_count = 0
        for grade in student.grades:
            if grade.subject == '文科':
                ranking_count += grade.total_ranking / liberal_arts_count
            else:
                ranking_count += grade.total_ranking / science_count
        ranking_avg = ranking_count / len(student.grades)
        new = AnalysisStudent(ranking_avg)
        new.student = student
        db.session.add(new)
        db.session.commit()


set_level()
