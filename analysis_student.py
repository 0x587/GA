from app.models import db, Student, Test

grades = Test.query.order_by(Test.test_time.desc()).first().Grade
liberal_arts_count = len([g for g in grades if g.Subject == '文科'])
science_count = len([g for g in grades if g.Subject == '理科'])
print(liberal_arts_count, science_count)
for student in Student.query.all():
    ranking_count = 0
    for grade in grades:
        if grade.Subject == '文科':
            ranking_count += grade.TotalRanking / liberal_arts_count
        else:
            ranking_count += grade.TotalRanking / science_count
    ranking_avg = ranking_count / len(student.Grade)
    print(ranking_avg, student)
