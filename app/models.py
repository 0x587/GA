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
