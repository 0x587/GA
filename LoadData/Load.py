from app.models import Test, StudentGrade
from app import db
import re
import os
from LoadData.LoadFile import load_file
from LoadData.ClassRanking import sort_class_ranking
from LoadData.StudentAnalysis import set_level
from LoadData.TestAnalysis import analysis_test


def sort_total_ranking():
    for test in Test.query.all():
        for subject in ['文科', '理科']:
            infos = []
            grades = StudentGrade.query.filter_by(test_time=test.test_time,
                                                  subject=subject).order_by(StudentGrade.total.desc()).all()
            for i, g in enumerate(grades):
                infos.append({'index': i + 1, 'total': g.total, 'grade': g})
            for index, info in enumerate(infos):
                if info['total'] == infos[index - 1]['total']:
                    info['index'] = infos[index - 1]['index']
            for info in infos:
                info['grade'].total_ranking = info['index']
            db.session.commit()


path = '../DataFile'
files = []
for root, _, filename in os.walk(path):
    for name in filename:
        files.append({'Root': root, 'Name': name})
if __name__ == '__main__':
    files.sort(key=lambda x: re.findall(r'[0-9]{8}', x['Name'])[0])
    for file in files:
        if os.path.splitext(file['Name'])[1].endswith('xlsx') or \
                os.path.splitext(file['Name'])[1].endswith('xls'):
            fileInfo = {'Root': (file['Root'] + '/' + file['Name']).replace('\\', r'/'),
                        'Name': file['Name']}
            load_file(fileInfo)
    print('Start sort personal ranking')
    sort_total_ranking()
    print('Start sort class ranking')
    sort_class_ranking()
    print('Start analysis student')
    set_level()
    print('Start analysis test')
    analysis_test()
