from app import db


class Class(db.Model):
    __tablename__ = "classes"

    index = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return 'Class:{}'.format(self.index)


class Student(db.Model):
    __tablename__ = "students"

    student_name = db.Column(db.String(8), primary_key=True)
    class_index = db.Column(db.ForeignKey('classes.index'))
    class_ = db.relationship('Class', backref='students')

    def __repr__(self):
        return self.student_name


class Test(db.Model):
    __tablename__ = 'tests'

    test_time = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(20))

    def __repr__(self):
        return '{}in{}'.format(self.test_name, self.test_time)


class Grade(db.Model):
    __tablename__ = 'grades'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)

    class_index = db.Column(db.Integer)

    student_name = db.Column(db.String(8), db.ForeignKey('students.student_name'))
    student = db.relationship('Student', backref='grades')

    subject = db.Column(db.String(2))

    test_time = db.Column(db.Integer, db.ForeignKey('tests.test_time'))
    test = db.relationship('Test', backref='grades')

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

    def __repr__(self):
        back1 = '语文:%s 数学:%s 英语:%s ' % (str(self.chinese), str(self.match), str(self.english))
        if self.subject == '文' or '文科':
            back2 = '政治:%s 历史:%s 地理:%s ' % (str(self.politics), str(self.history), str(self.geography))
        else:
            back2 = '物理:%s 化学:%s 生物:%s ' % (str(self.physics), str(self.chemistry), str(self.biology))
        back = back1 + back2
        return back
