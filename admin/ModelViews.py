from flask_admin.contrib.sqla import ModelView
from app.models import *


class TestView(ModelView):
    can_delete = False
    page_size = 15


class TeacherView(ModelView):
    can_delete = False
    page_size = 15


class ClassView(ModelView):
    can_delete = False
    page_size = 15
    column_list = [Class.index]


class StudentView(ModelView):
    can_delete = False
    page_size = 15


class StudentGradeView(ModelView):
    can_delete = False
    page_size = 6


class ClassAverageGradeView(ModelView):
    can_delete = False
    page_size = 6


class TestHighGradeView(ModelView):
    can_delete = False
    page_size = 6


class TestAverageGradeView(ModelView):
    can_delete = False
    page_size = 6
