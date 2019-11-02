from app.models import *


def set_level():
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
