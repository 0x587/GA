from admin.ModelViews import *
from app import admin, models, db

admin.add_view(TeacherView(models.Teacher, db.session))
admin.add_view(StudentView(models.Student, db.session, category="Student"))
admin.add_view(StudentGradeView(models.StudentGrade, db.session, category="Student"))
admin.add_view(ClassView(models.Class, db.session, category="Class"))
admin.add_view(ClassAverageGradeView(models.ClassAverageGrade, db.session, category="Class"))
admin.add_view(TestView(models.Test, db.session, category="Test"))
admin.add_view(TestAverageGradeView(models.TestAverageGrade, db.session, category="Test"))
admin.add_view(TestHighGradeView(models.TestHighGrade, db.session, category="Test"))
