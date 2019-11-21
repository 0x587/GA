def student_type(class_index: int) -> str:
    """
    返回学生类型。
    :param class_index:
    :return: student_type
    :rtype: str
    """
    if class_index in [1809, 1810]:
        return 'Experiment Student'
    else:
        return 'Ordinary Student'


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
