from app import db
from Level import avg2level


class Class(db.Model):
    __tablename__ = "classes"

    index = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return 'Class:{}'.format(self.index)


class Student(db.Model):
    __tablename__ = "students"

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_name = db.Column(db.String(8))
    test_id = db.Column(db.Integer)
    class_index = db.Column(db.ForeignKey('classes.index'))
    class_ = db.relationship('Class', backref='students')

    def __repr__(self):
        return self.student_name


class Teacher(db.Model):
    __tablename__ = "teachers"

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teacher_name = db.Column(db.String(8))
    subject = db.Column(db.String(8))


class Test(db.Model):
    __tablename__ = 'tests'

    test_time = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(20))

    def __repr__(self):
        return '{}in{}'.format(self.test_name, self.test_time)


class GradeBaseNoRanking(db.Model):
    __abstract__ = True

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject = db.Column(db.String(2))

    chinese = db.Column(db.Float)
    math = db.Column(db.Float)
    english = db.Column(db.Float)
    physics = db.Column(db.Float)
    chemistry = db.Column(db.Float)
    biology = db.Column(db.Float)
    geography = db.Column(db.Float)
    politics = db.Column(db.Float)
    history = db.Column(db.Float)
    total = db.Column(db.Float)

    def grade_dict(self):
        return {'subject': self.subject,
                'chinese': self.chinese, 'math': self.math, 'english': self.english,
                'biology': self.biology, 'physics': self.physics, 'chemistry': self.chemistry,
                'politics': self.politics, 'history': self.history, 'geography': self.geography,
                'total': self.total}

    def set_grade(self, subject: str, grade: int or float):
        if subject == 'chinese':
            self.chinese = grade
        elif subject == 'math':
            self.math = grade
        elif subject == 'english':
            self.english = grade
        elif subject == 'politics':
            self.politics = grade
        elif subject == 'history':
            self.history = grade
        elif subject == 'geography':
            self.geography = grade
        elif subject == 'physics':
            self.physics = grade
        elif subject == 'chemistry':
            self.chemistry = grade
        elif subject == 'biology':
            self.biology = grade
        elif subject == 'total':
            self.total = grade
        else:
            raise KeyError('This subject does not exist:{}'.format(subject))

    def __repr__(self):
        back1 = '语文:%s 数学:%s 英语:%s ' % (str(self.chinese), str(self.math), str(self.english))
        if self.subject == '文科':
            back2 = '政治:%s 历史:%s 地理:%s ' % (str(self.politics), str(self.history), str(self.geography))
        else:
            back2 = '物理:%s 化学:%s 生物:%s ' % (str(self.physics), str(self.chemistry), str(self.biology))
        back = back1 + back2
        return back


class GradeBase(GradeBaseNoRanking):
    __abstract__ = True

    chinese_ranking = db.Column(db.Integer)
    math_ranking = db.Column(db.Integer)
    english_ranking = db.Column(db.Integer)
    physics_ranking = db.Column(db.Integer)
    chemistry_ranking = db.Column(db.Integer)
    biology_ranking = db.Column(db.Integer)
    geography_ranking = db.Column(db.Integer)
    politics_ranking = db.Column(db.Integer)
    history_ranking = db.Column(db.Integer)
    total_ranking = db.Column(db.Integer)

    def set_ranking(self, subject: str, ranking: int):
        if subject == 'chinese':
            self.chinese_ranking = ranking
        elif subject == 'math':
            self.math_ranking = ranking
        elif subject == 'english':
            self.english_ranking = ranking
        elif subject == 'politics':
            self.politics_ranking = ranking
        elif subject == 'history':
            self.history_ranking = ranking
        elif subject == 'geography':
            self.geography_ranking = ranking
        elif subject == 'physics':
            self.physics_ranking = ranking
        elif subject == 'chemistry':
            self.chemistry_ranking = ranking
        elif subject == 'biology':
            self.biology_ranking = ranking
        elif subject == 'total':
            self.total_ranking = ranking
        else:
            raise KeyError('This subject does not exist:{}'.format(subject))


class ClassAverageGrade(GradeBase):
    __tablename__ = 'class_average_grades'

    test_time = db.Column(db.Integer, db.ForeignKey('tests.test_time'))
    test = db.relationship('Test', backref='class_average_grades')

    class_index = db.Column(db.Integer, db.ForeignKey('classes.index'))
    class_ = db.relationship('Class', backref='class_average_grades')

    def __init__(self, class_index: int):
        self.class_ = Class.query.filter_by(index=class_index).first()

    def limit_subject(self, limit_type='best'):
        if self.subject == '文科':
            dic = {'chinese': self.chinese_ranking, 'math': self.math_ranking, 'english': self.english_ranking,
                   'politics': self.politics_ranking, 'history': self.history_ranking,
                   'geography': self.geography_ranking,
                   }
        else:
            dic = {'chinese': self.chinese_ranking, 'math': self.math_ranking, 'english': self.english_ranking,
                   'biology': self.biology_ranking, 'physics': self.physics_ranking,
                   'chemistry': self.chemistry_ranking,
                   }
        if limit_type == 'best':
            return min(dic, key=dic.get)
        elif limit_type == 'worse':
            return max(dic, key=dic.get)
        else:
            raise Warning('limit type is unlawful')


class StudentGrade(GradeBase):
    __tablename__ = 'student_grades'

    test_time = db.Column(db.Integer, db.ForeignKey('tests.test_time'))
    test = db.relationship('Test', backref='student_grades')

    student_ID = db.Column(db.Integer, db.ForeignKey('students.ID'))
    student = db.relationship('Student', backref='student_grades')

    class_index = db.Column(db.Integer)

    def grade_dict(self):
        return {'subject': self.subject,
                'chinese': self.chinese, 'math': self.math, 'english': self.english,
                'biology': self.biology, 'physics': self.physics, 'chemistry': self.chemistry,
                'politics': self.politics, 'history': self.history, 'geography': self.geography,
                'total': self.total, 'ID': self.student_ID}

    def get_this_level(self, total: int) -> str:
        avg = self.total_ranking / total
        return avg2level(avg)


class TestHighGrade(GradeBase):
    __tablename__ = 'test_high_grades'

    test_time = db.Column(db.Integer, db.ForeignKey('tests.test_time'))
    test = db.relationship('Test', backref='test_high_grades')

    def __init__(self, test: Test):
        self.test = test


class TestAverageGrade(GradeBase):
    __tablename__ = 'test_average_grades'

    test_time = db.Column(db.Integer, db.ForeignKey('tests.test_time'))
    test = db.relationship('Test', backref='test_average_grades')

    def __init__(self, test: Test):
        self.test = test


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
        return avg2level(avg)
