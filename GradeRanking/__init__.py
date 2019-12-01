from app.models import StudentGrade, Test
from app import db


def grade2ranking(test: Test, grade: int, subject: str = 'total', subject_type: str = '理科') -> int:
    """
    查找本次考试此分数对应(或最相近)的排名。
    :param test: 需要查找的考试
    :param grade: 分数
    :param subject_type:理科or文科
    :param subject:查找的科目
    :return:ranking
    """
    limit = 0
    limit_flag = True
    result = None
    while limit_flag:
        result = StudentGrade.query.filter(
            StudentGrade.test_time == test.test_time,
            StudentGrade.__dict__[subject].between(grade - limit, grade + limit),
            StudentGrade.subject == subject_type
        ).all()
        if result:
            limit_flag = False
        else:
            limit += 1
    return result[0].__dict__[subject + '_ranking']


def grade2ranking_with_grade(grade_id: int, subject: str = 'total') -> int:
    """
    查找本次考试此分数对应(或最相近)的排名。
    :param grade_id: Grade对象id
    :param subject: 查找的科目
    :return: ranking
    """
    grade = StudentGrade.query.filter_by(ID=grade_id).first()
    grades = [g[0] for g in db.session.query(StudentGrade.__dict__[subject]).filter_by(
        test_time=grade.test_time, subject=grade.subject).order_by(
        StudentGrade.__dict__[subject].desc()).all()]

    return grades.index(grade.__dict__[subject]) + 1


def grade2ranking_for_class(grade_id: int, subject: str = 'total') -> int:
    """
    查找本次考试此分数对应(或最相近)的班级排名。
    :param grade_id: Grade对象id
    :param subject:查找的科目
    :return:ranking
    """
    grade = StudentGrade.query.filter_by(ID=grade_id).first()
    grades = [g[0] for g in
              db.session.query(StudentGrade.__dict__[subject]).filter_by(
                  test_time=grade.test_time, class_index=grade.class_index).order_by(
                  StudentGrade.__dict__[subject].desc()).all()]

    return grades.index(grade.__dict__[subject]) + 1


def grade_rate(grades: list, grade_line: int or float) -> float:
    target = [g for g in grades if g >= grade_line]
    return len(target) / len(grades)


def avg2level(avg: float) -> str:
    if 0 < avg <= 0.05:
        return 'A+'
    elif 0.05 < avg <= 0.25:
        return 'A'
    elif 0.25 < avg <= 0.50:
        return 'B+'
    elif 0.50 < avg <= 0.75:
        return 'B'
    elif 0.75 < avg <= 0.95:
        return 'C+'
    elif 0.95 < avg <= 1:
        return 'C'


def get_level_description():
    return 'A+:0%-5%; A:5%-25%; B+:25%-50%; B:50%-75%; C+:70%-95%; C:95%-100%; '
