from app.models import *
import numpy as np

high_line = 80
for test in Test.query.all():
    for subject_class in ['文科', '理科']:
        average_grade = TestAverageGrade(test)
        average_grade.subject = subject_class
        high_grade = TestHighGrade(test)
        high_grade.subject = subject_class
        db.session.add(average_grade)
        db.session.add(high_grade)
        grades = StudentGrade.query.filter_by(
            subject=subject_class, test_time=test.test_time).all()
        must_subject = ['chinese', 'match', 'english', 'total']
        if subject_class == '文科':
            subjects = must_subject + ['politics', 'history', 'geography']
        else:
            subjects = must_subject + ['physics', 'chemistry', 'biology']
        for subject in subjects:
            grade_array = np.array([g.grade_dict()[subject] for g in grades])
            average_grade.set_grade(subject, float(round(np.average(grade_array), 2)))
            high_grade.set_grade(subject, float(round(np.percentile(grade_array, high_line), 2)))
        db.session.commit()
