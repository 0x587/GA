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
