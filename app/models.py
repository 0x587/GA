from app import db


class Student(db.Model):
    __tablename__ = "students"

    test_id = db.Column(db.Integer)
    student_name = db.Column(db.String(8), primary_key=True)
    class_index = db.Column(db.Integer)

    def __repr__(self):
        late_test = db.session.query(Grade).filter_by(StudentName=self.student_name).ordey_by(
            Grade.TestTime.desc()
        ).first()
        return (
                '/***************************************' + '\n' +
                ('student_name: %s' % self.student_name) + '\n' +
                ('test_id: %s' % self.test_id) + '\n' +
                ('class_index: %s' % self.class_index) + '\n' +
                # ('StudentGrade: %s' % self.StudentGrade)
                '***************************************/' + '\n'
        )


class Grade(db.Model):
    __tablename__ = 'grades'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)

    class_index = db.Column(db.Integer)

    StudentName = db.Column(db.String(8), db.ForeignKey('students.student_name'))
    Student = db.relationship('Student', backref='Grade')

    Subject = db.Column(db.String(2))

    TestTime = db.Column(db.Integer, db.ForeignKey('tests.test_time'))
    test = db.relationship('Test', backref='Grade')

    Chinese = db.Column(db.Float)
    ChineseRanking = db.Column(db.Integer)
    Match = db.Column(db.Float)
    MatchRanking = db.Column(db.Integer)
    English = db.Column(db.Float)
    EnglishRanking = db.Column(db.Integer)
    Physics = db.Column(db.Float)
    PhysicsRanking = db.Column(db.Integer)
    Chemistry = db.Column(db.Float)
    ChemistryRanking = db.Column(db.Integer)
    Biology = db.Column(db.Float)
    BiologyRanking = db.Column(db.Integer)
    Geography = db.Column(db.Float)
    GeographyRanking = db.Column(db.Integer)
    Politics = db.Column(db.Float)
    PoliticsRanking = db.Column(db.Integer)
    History = db.Column(db.Float)
    HistoryRanking = db.Column(db.Integer)
    Total = db.Column(db.Float)
    TotalRanking = db.Column(db.Integer)

    def __repr__(self):
        back1 = '语文:%s 数学:%s 英语:%s ' % (str(self.Chinese), str(self.Match), str(self.English))
        if self.Subject == '文' or '文科':
            back2 = '政治:%s 历史:%s 地理:%s ' % (str(self.Politics), str(self.History), str(self.Geography))
        else:
            back2 = '物理:%s 化学:%s 生物:%s ' % (str(self.Physics), str(self.Chemistry), str(self.Biology))
        back = back1 + back2
        return back


class Test(db.Model):
    __tablename__ = 'tests'

    test_time = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(20))
