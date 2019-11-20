from app.models import StudentGrade, Test


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
