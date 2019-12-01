from app.models import StudentGrade


def must_subject(include_total: bool = True) -> list:
    """
    返回必修科目。
    :param include_total:
    :return: must_subject
    :rtype: list
    """
    if include_total:
        return ['chinese', 'match', 'english', 'total']
    else:
        return ['chinese', 'match', 'english']


def li_subject() -> list:
    """
    返回理科科目。
    :return: li_subject
    """
    return ['physics', 'chemistry', 'biology']


def li_all_subject(include_total: bool = True) -> list:
    """
    返回理科全部科目。
    :param include_total:
    :return: subjects
    """
    subjects = must_subject(include_total)
    subjects[3:2] = li_subject()
    return subjects


def wen_subject() -> list:
    """
    返回文科科目。
    :return: wen_subject
    """
    return ['politics', 'history', 'geography']


def wen_all_subject(include_total: bool = True) -> list:
    """
    返回文科全部科目。
    :param include_total:
    :return: subjects
    """
    subjects = must_subject(include_total)
    subjects[3:2] = wen_subject()
    return subjects


def subjects_by_grade(grade: StudentGrade) -> list:
    """
    通过传入的Grade对象判断返回科目列表。
    :param grade:
    :return: subjects
    """
    return wen_all_subject() \
        if grade.subject == '文科' \
        else li_all_subject()


def subject_full_grade(subject: str) -> int:
    if subject in must_subject(False):
        return 150
    elif subject == 'total':
        return 750
    else:
        return 100


def en2cn(subject: str) -> str:
    """
    学科名字英文译中文。
    :param subject: 英文名
    :return: subject_cn_name:中文名
    """
    if subject == 'chinese':
        return '语文'
    elif subject == 'match':
        return '数学'
    elif subject == 'english':
        return '数学'
    elif subject == 'physics':
        return '物理'
    elif subject == 'chemistry':
        return '化学'
    elif subject == 'biology':
        return '生物'
    elif subject == 'politics':
        return '政治'
    elif subject == 'history':
        return '历史'
    elif subject == 'geography':
        return '地理'
    else:
        raise KeyError('This subject is no exist')
