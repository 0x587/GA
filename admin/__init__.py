from flask_admin.contrib.sqla import ModelView
from app import admin, models, db

admin.add_view(ModelView(models.Teacher, db.session))
admin.add_view(ModelView(models.Student, db.session, category="Student"))
admin.add_view(ModelView(models.StudentGrade, db.session, category="Student"))
admin.add_view(ModelView(models.Class, db.session, category="Class"))
admin.add_view(ModelView(models.ClassAverageGrade, db.session, category="Class"))
admin.add_view(ModelView(models.Test, db.session, category="Test"))
admin.add_view(ModelView(models.TestAverageGrade, db.session, category="Test"))
admin.add_view(ModelView(models.TestHighGrade, db.session, category="Test"))
