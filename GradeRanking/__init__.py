from app.models import StudentGrade, Test


def grade2ranking(test: Test, grade: int) -> int:
    """
    查找本次考试此分数对应(或最相近)的排名。
    :param test: 需要查找的考试
    :param grade: 分数
    :return:ranking
    """
    limit = 0
    limit_flag = True
    result = None
    while limit_flag:
        result = StudentGrade.query.filter(
            StudentGrade.test_time == test.test_time,
            StudentGrade.total.between(grade - limit, grade + limit)
        ).all()
        if result:
            limit_flag = False
        else:
            limit += 1
    return result[0].total_ranking
