import os
from LoadData.LoadFile import load_file
from app.models import *
import re


def sort_total_ranking():
    for test in Test.query.all():
        for subject in ['文科', '理科']:
            infos = []
            grades = Grade.query.filter_by(TestTime=test.test_time,
                                           Subject=subject).order_by(Grade.Total.desc()).all()
            for i, g in enumerate(grades):
                infos.append({'index': i + 1, 'total': g.Total, 'grade': g})
            for index, info in enumerate(infos):
                if info['total'] == infos[index - 1]['total']:
                    info['index'] = infos[index - 1]['index']
            for info in infos:
                info['grade'].TotalRanking = info['index']
            db.session.commit()


path = os.getcwd() + '/DataFile'
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
    print('Start sort ranking')
    sort_total_ranking()
