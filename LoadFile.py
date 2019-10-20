import xlrd
from app.models import Student, Grade, Test
import os
from time import time
from app.models import db


def my_filter(data):
    if data == '':
        return 0
    else:
        return int(data)


def load_students(workbook):
    old_student_name = []
    old_students = db.session.query(Student).all()
    for student in old_students:
        old_student_name.append(student.student_name)
    for sheet_name in ['文科', '理科']:
        worksheet = workbook.sheet_by_name(sheet_name)
        new_students = []
        for index in range(1, worksheet.nrows):
            work_row = worksheet.row_values(index)
            if db.session.query(Student).filter_by(student_name=work_row[2]).all():
                # exist
                current_st = db.session.query(Student).filter_by(student_name=work_row[2]).first()
            else:
                # new
                current_st = Student()
                db.session.add(current_st)
            current_st.class_index = work_row[0][0:4]
            current_st.student_name = work_row[2]
            current_st.test_id = work_row[0]
            new_students.append(current_st)
        db.session.commit()


def load_grade(work_file: dict, workbook):
    if work_file['Name'][15] == '1':
        test_name = work_file['Name'][10:14] + '-上学期'
    else:
        test_name = work_file['Name'][10:14] + '-下学期'
    if not db.session.query(Test).filter_by(test_name=test_name).all():
        current_test = Test()
        current_test.test_name = test_name
        current_test.test_time = os.path.splitext(work_file['Name'])[0][22:30]
        db.session.add(current_test)
    else:
        current_test = db.session.query(Test).filter_by(test_name=test_name).first()
    for sheet_name in ['文科', '理科']:
        worksheet = workbook.sheet_by_name(sheet_name)
        for index in range(1, worksheet.nrows):
            work_row = worksheet.row_values(index)
            new_grade = Grade()
            new_grade.test = current_test
            new_grade.Student = db.session.query(Student).filter_by(
                student_name=work_row[worksheet.row_values(0).index('姓名')]).first()
            new_grade.class_index = work_row[worksheet.row_values(0).index('班级')]
            new_grade.Subject = sheet_name
            new_grade.TestTime = os.path.splitext(work_file['Name'])[0][22:30]
            new_grade.Chinese = my_filter(work_row[worksheet.row_values(0).index('语文')])
            new_grade.ChineseRanking = my_filter(work_row[worksheet.row_values(0).index('语文') + 1])
            new_grade.Match = my_filter(work_row[worksheet.row_values(0).index('数学')])
            new_grade.MatchRanking = my_filter(work_row[worksheet.row_values(0).index('数学') + 1])
            new_grade.English = my_filter(work_row[worksheet.row_values(0).index('英语')])
            new_grade.EnglishRanking = my_filter(work_row[worksheet.row_values(0).index('英语') + 1])
            new_grade.Total = new_grade.Chinese + new_grade.Match + new_grade.English
            if str(new_grade.Subject) == '理科':
                new_grade.Physics = my_filter(work_row[worksheet.row_values(0).index('物理')])
                new_grade.Chemistry = my_filter(work_row[worksheet.row_values(0).index('化学')])
                new_grade.Biology = my_filter(work_row[worksheet.row_values(0).index('生物')])
                new_grade.PhysicsRanking = my_filter(work_row[worksheet.row_values(0).index('物理') + 1])
                new_grade.ChemistryRanking = my_filter(work_row[worksheet.row_values(0).index('化学') + 1])
                new_grade.BiologyRanking = my_filter(work_row[worksheet.row_values(0).index('生物') + 1])
                new_grade.Total += new_grade.Physics + new_grade.Chemistry + new_grade.Biology
            else:
                new_grade.Politics = my_filter(work_row[worksheet.row_values(0).index('政治')])
                new_grade.History = my_filter(work_row[worksheet.row_values(0).index('历史')])
                new_grade.Geography = my_filter(work_row[worksheet.row_values(0).index('地理')])
                new_grade.PoliticsRanking = my_filter(work_row[worksheet.row_values(0).index('政治') + 1])
                new_grade.HistoryRanking = my_filter(work_row[worksheet.row_values(0).index('历史') + 1])
                new_grade.GeographyRanking = my_filter(work_row[worksheet.row_values(0).index('地理') + 1])
                new_grade.Total += new_grade.Politics + new_grade.Geography + new_grade.History
            db.session.add(new_grade)
    db.session.commit()


def load_file(work_file: dict):
    stime = time()
    if work_file['Name'][15] == '1':
        print('Start Load :%s' % (work_file['Name'][10:14]) + '-上学期')
    else:
        print('Start Load :%s' % (work_file['Name'][10:14]) + '-下学期')
    workbook = xlrd.open_workbook(work_file['Root'])
    load_students(workbook)
    load_grade(work_file, workbook)
    print('Spend %f S' % (time() - stime))
