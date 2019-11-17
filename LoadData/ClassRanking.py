from app import db
from app.models import Test, StudentGrade, ClassAverageGrade


def sort_class_ranking():
    for test in Test.query.all():
        class_infos = {index: {'obj': ClassAverageGrade(index),
                               'grades': []} for index in range(1801, 1821)}
        for grade in StudentGrade.query.filter(StudentGrade.test_time == test.test_time).all():
            class_infos[grade.class_index]['grades'].append(grade.grade_dict())
        for key, value in class_infos.items():
            try:
                obj: ClassAverageGrade = value['obj']
                obj.subject = value['grades'][0]['subject']
                obj.test = test
                obj.total = sum([v['total'] for v in value['grades']]) / len(value['grades'])
                obj.chinese = sum([v['chinese'] for v in value['grades']]) / len(value['grades'])
                obj.match = sum([v['match'] for v in value['grades']]) / len(value['grades'])
                obj.english = sum([v['english'] for v in value['grades']]) / len(value['grades'])
                if value['grades'][0]['subject'] == '理科':
                    obj.physics = sum([v['physics'] for v in value['grades']]) / len(value['grades'])
                    obj.chemistry = sum([v['chemistry'] for v in value['grades']]) / len(value['grades'])
                    obj.biology = sum([v['biology'] for v in value['grades']]) / len(value['grades'])
                else:
                    obj.politics = sum([v['politics'] for v in value['grades']]) / len(value['grades'])
                    obj.history = sum([v['history'] for v in value['grades']]) / len(value['grades'])
                    obj.geography = sum([v['geography'] for v in value['grades']]) / len(value['grades'])
                db.session.add(obj)
            except Exception as e:
                print(e)
        db.session.commit()

    for test in Test.query.all():
        for subject in ['文科', '理科']:
            # Chinese
            for i, g in enumerate(ClassAverageGrade.query.filter_by(
                    test_time=test.test_time,
                    subject=subject).order_by(ClassAverageGrade.chinese).all()):
                g.chinese_ranking = 17 - i
            # Match
            for i, g in enumerate(ClassAverageGrade.query.filter_by(
                    test_time=test.test_time,
                    subject=subject).order_by(ClassAverageGrade.match).all()):
                g.match_ranking = 17 - i
            # English
            for i, g in enumerate(ClassAverageGrade.query.filter_by(
                    test_time=test.test_time,
                    subject=subject).order_by(ClassAverageGrade.english).all()):
                g.english_ranking = 17 - i
            if subject == '理科':
                # Physics
                for i, g in enumerate(ClassAverageGrade.query.filter_by(
                        test_time=test.test_time,
                        subject=subject).order_by(ClassAverageGrade.physics).all()):
                    g.physics_ranking = 17 - i
                # Chemistry
                for i, g in enumerate(ClassAverageGrade.query.filter_by(
                        test_time=test.test_time,
                        subject=subject).order_by(ClassAverageGrade.chemistry).all()):
                    g.chemistry_ranking = 17 - i
                # Biology
                for i, g in enumerate(ClassAverageGrade.query.filter_by(
                        test_time=test.test_time,
                        subject=subject).order_by(ClassAverageGrade.biology).all()):
                    g.biology_ranking = 17 - i
            else:
                # Politics
                for i, g in enumerate(ClassAverageGrade.query.filter_by(
                        test_time=test.test_time,
                        subject=subject).order_by(ClassAverageGrade.politics).all()):
                    g.politics_ranking = 17 - i
                # History
                for i, g in enumerate(ClassAverageGrade.query.filter_by(
                        test_time=test.test_time,
                        subject=subject).order_by(ClassAverageGrade.history).all()):
                    g.history_ranking = 17 - i
                # Geography
                for i, g in enumerate(ClassAverageGrade.query.filter_by(
                        test_time=test.test_time,
                        subject=subject).order_by(ClassAverageGrade.geography).all()):
                    g.geography_ranking = 17 - i
            # Total
            for i, g in enumerate(ClassAverageGrade.query.filter_by(
                    test_time=test.test_time,
                    subject=subject).order_by(ClassAverageGrade.total).all()):
                g.total_ranking = 17 - i

                db.session.commit()
