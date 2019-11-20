from app.models import *
import numpy as np
import Subject
from GradeRanking import grade2ranking

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
        if subject_class == '文科':
            subjects = Subject.wen_all_subject(True)
        else:
            subjects = Subject.li_all_subject(True)
        for subject in subjects:
            grade_array = np.array([g.grade_dict()[subject] for g in grades])
            average_grade.set_grade(subject, float(round(np.average(grade_array), 2)))
            average_grade.set_ranking(subject, grade2ranking(
                test, int(np.average(grade_array)),
                subject=subject, subject_type=subject_class))
            high_grade.set_grade(subject, float(round(np.percentile(grade_array, high_line), 2)))
            high_grade.set_ranking(subject, grade2ranking(
                test, int(np.percentile(grade_array, high_line)),
                subject=subject, subject_type=subject_class))
        db.session.commit()
