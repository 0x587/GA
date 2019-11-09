from LoadData.DataModels import *


class AnalysisStudent(db.Model):
    __tablename__ = 'analysis_students'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)

    avg = db.Column(db.Float)
    student_ID = db.Column(db.Integer, db.ForeignKey('students.ID'))
    student = db.relationship('Student', backref='analysis')

    def __init__(self, avg: float):
        self.avg = avg

    def get_level(self):
        avg = self.avg
        if 0 < avg <= 0.15:
            return 'top'
        elif 0.15 < avg <= 0.45:
            return 'high'
        elif 0.45 < avg <= 0.75:
            return 'medium'
        elif 0.75 < avg <= 1:
            return 'low'


class ClassAverageGrade(db.Model):
    __tablename__ = 'class_avg_grades'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)

    class_index = db.Column(db.Integer, db.ForeignKey('classes.index'))
    class_ = db.relationship('Class', backref='class_avg_grade')

    subject = db.Column(db.String(2))

    test_time = db.Column(db.Integer, db.ForeignKey('tests.test_time'))
    test = db.relationship('Test', backref='class_avg_grades')

    chinese = db.Column(db.Float)
    chinese_ranking = db.Column(db.Integer)
    match = db.Column(db.Float)
    match_ranking = db.Column(db.Integer)
    english = db.Column(db.Float)
    english_ranking = db.Column(db.Integer)
    physics = db.Column(db.Float)
    physics_ranking = db.Column(db.Integer)
    chemistry = db.Column(db.Float)
    chemistry_ranking = db.Column(db.Integer)
    biology = db.Column(db.Float)
    biology_ranking = db.Column(db.Integer)
    geography = db.Column(db.Float)
    geography_ranking = db.Column(db.Integer)
    politics = db.Column(db.Float)
    politics_ranking = db.Column(db.Integer)
    history = db.Column(db.Float)
    history_ranking = db.Column(db.Integer)
    total = db.Column(db.Float)
    total_ranking = db.Column(db.Integer)

    def __init__(self, class_index: int):
        self.class_ = Class.query.filter_by(index=class_index).first()
