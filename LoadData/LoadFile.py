from app.models import Class, Student, Test, StudentGrade
from app import db
from time import time
import xlrd
import os


def check_personnel_adjustments(workbook):
    # 获取本次考试所以学生信息
    students: list = []
    for sheet_name in ['文科', '理科']:
        worksheet = workbook.sheet_by_name(sheet_name)
        for index in range(1, worksheet.nrows):
            student = {}
            work_row = worksheet.row_values(index)
            student['class_index'] = work_row[0][0:4]
            student['student_name'] = work_row[2]
            student['test_id'] = work_row[0]
            students.append(student)
    # 对每个班级库中信息作对比
    for class_index in range(1801, 1821):
        # 检查该班级是否已在库中
        if not Class.query.filter_by(index=class_index).all():
            db.session.add(Class(index=class_index))
            db.session.commit()
        current_students = [s for s in students if s['class_index'] == str(class_index)]
        exist_students = Student.query.filter_by(class_index=class_index).all()

        for new_student in current_students:
            # 排除此人 有重名 手动导入
            if new_student['student_name'] != '李舒婷':
                # 该班级原来没有的人
                if not [s for s in exist_students if s.student_name == new_student['student_name']]:
                    query_result = Student.query.filter_by(student_name=new_student['student_name']).all()
                    if not query_result:
                        print('新生转入: {}班新增{}'.format(class_index, new_student['student_name']))
                        # 新生注册
                        student = Student()
                        student.student_name = str(new_student['student_name'])
                        student.class_index = int(new_student['class_index'])
                        student.test_id = int(new_student['test_id'])
                        db.session.add(student)
                        db.session.commit()
                    else:
                        old_class_index = query_result[0].class_index
                        query_result[0].class_index = class_index
                        db.session.commit()
                        print('流动管理: {}班新增{},旧班级{}'.format(class_index,
                                                           new_student['student_name'], old_class_index))


def my_filter(data):
    if data == '':
        return 0
    else:
        return int(data)


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
            new_grade = StudentGrade()
            new_grade.test = current_test
            new_grade.student = db.session.query(Student).filter_by(
                student_name=work_row[worksheet.row_values(0).index('姓名')]).first()
            new_grade.class_index = work_row[worksheet.row_values(0).index('班级')]
            new_grade.subject = sheet_name
            new_grade.test_time = os.path.splitext(work_file['Name'])[0][22:30]
            new_grade.chinese = my_filter(work_row[worksheet.row_values(0).index('语文')])
            new_grade.chinese_ranking = my_filter(work_row[worksheet.row_values(0).index('语文') + 1])
            new_grade.match = my_filter(work_row[worksheet.row_values(0).index('数学')])
            new_grade.match_ranking = my_filter(work_row[worksheet.row_values(0).index('数学') + 1])
            new_grade.english = my_filter(work_row[worksheet.row_values(0).index('英语')])
            new_grade.english_ranking = my_filter(work_row[worksheet.row_values(0).index('英语') + 1])
            new_grade.total = new_grade.chinese + new_grade.match + new_grade.english
            if str(new_grade.subject) == '理科':
                new_grade.physics = my_filter(work_row[worksheet.row_values(0).index('物理')])
                new_grade.chemistry = my_filter(work_row[worksheet.row_values(0).index('化学')])
                new_grade.biology = my_filter(work_row[worksheet.row_values(0).index('生物')])
                new_grade.physics_ranking = my_filter(work_row[worksheet.row_values(0).index('物理') + 1])
                new_grade.chemistry_ranking = my_filter(work_row[worksheet.row_values(0).index('化学') + 1])
                new_grade.biology_ranking = my_filter(work_row[worksheet.row_values(0).index('生物') + 1])
                new_grade.total += new_grade.physics + new_grade.chemistry + new_grade.biology
            else:
                new_grade.politics = my_filter(work_row[worksheet.row_values(0).index('政治')])
                new_grade.history = my_filter(work_row[worksheet.row_values(0).index('历史')])
                new_grade.geography = my_filter(work_row[worksheet.row_values(0).index('地理')])
                new_grade.politics_ranking = my_filter(work_row[worksheet.row_values(0).index('政治') + 1])
                new_grade.history_ranking = my_filter(work_row[worksheet.row_values(0).index('历史') + 1])
                new_grade.geography_ranking = my_filter(work_row[worksheet.row_values(0).index('地理') + 1])
                new_grade.total += new_grade.politics + new_grade.geography + new_grade.history
            db.session.add(new_grade)
    db.session.commit()


def load_file(current_file_info: dict):
    stime = time()
    if current_file_info['Name'][15] == '1':
        print('Start Load :%s' % (current_file_info['Name'][10:14]) + '-上学期')
    else:
        print('Start Load :%s' % (current_file_info['Name'][10:14]) + '-下学期')
    # 打开文件
    current_book = xlrd.open_workbook(current_file_info['Root'])
    check_personnel_adjustments(current_book)
    load_grade(current_file_info, current_book)
    print('Spend %f S' % (time() - stime))
