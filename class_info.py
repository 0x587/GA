from app.models import *


def student_count(class_index: int):
    lats_test_time = db.session.query(db.func.max(Test.test_time)).scalar()
    return db.session.query(Grade).filter_by(TestTime=lats_test_time,
                                             class_index=class_index).count()


def newest_data():
    lats_test_time = str(db.session.query(db.func.max(Test.test_time)).scalar())
    return '{}-{}-{} {}'.format(
        lats_test_time[0:4], lats_test_time[4:6], lats_test_time[6:8],
        Test.query.filter_by(test_time=int(lats_test_time)).first().test_name)


def now_student(class_index: int) -> list:
    lats_test_time = str(db.session.query(db.func.max(Test.test_time)).scalar())
    grades = db.session.query(Grade).filter_by(TestTime=lats_test_time,
                                               class_index=class_index).all()
    return [s.ID for s in grades]


def class_ranking(test_time: int) -> dict:
    grades = db.session.query(Grade).filter_by(TestTime=test_time).all()
    classes = {}
    for i in range(1801, 1818):
        classes[i] = 0
    for key in classes:
        pass