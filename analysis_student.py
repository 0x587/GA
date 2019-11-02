from app.models import db, Student, Test

grades = Test.query.order_by(Test.test_time.desc()).first().grades
liberal_arts_count = len([g for g in grades if g.subject == '文科'])
science_count = len([g for g in grades if g.subject == '理科'])
print(liberal_arts_count, science_count)
for student in Student.query.all():
    ranking_count = 0
    for grade in student.grades:
        if grade.subject == '文科':
            ranking_count += grade.total_ranking / liberal_arts_count
        else:
            ranking_count += grade.total_ranking / science_count
    ranking_avg = ranking_count / len(student.grades)
    print(ranking_avg, student)
