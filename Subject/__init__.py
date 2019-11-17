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
    :return: li_all_subject
    """
    return must_subject(include_total) + li_subject()


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
    :return: wen_all_subject
    """
    return must_subject(include_total) + wen_subject()
