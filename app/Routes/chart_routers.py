from app import app
from AnalysisData.Class import class_history_grade, class_grade_distributed
from AnalysisData.Student.charts import student_grade_radar, student_grade_compared, student_history_ranking
from AnalysisData.Test import test_grade_distributed_chart, test_avg_grade_compare, \
    test_student_distributed, test_high_grade_distributed
from app.models import *
import json


@app.route('/charts/student_history_ranking/<int:student_id>')
def student_history_ranking_chart(student_id: int):
    print(student_id)
    data = student_history_ranking(student_id)
    result = {}
    for key, value in data.items():
        result[key] = json.loads(value.dump_options())
    return json.dumps(result)


@app.route('/charts/history_grade_chart/<int:class_index>')
def history_grade_chart(class_index: int):
    return class_history_grade(
        class_index).dump_options_with_quotes()


@app.route('/charts/distributed_chart/<int:class_index>')
def distributed_chart(class_index: int):
    return class_grade_distributed(
        class_index)[0].dump_options_with_quotes()


@app.route('/charts/grade_compared_chart/<int:grade_id>')
def grade_compared_chart(grade_id: int):
    return student_grade_compared(
        StudentGrade.query.filter_by(ID=grade_id).first()).dump_options_with_quotes()


@app.route('/charts/ranking_radar_chart/<int:grade_id>')
def ranking_radar_chart(grade_id: int):
    return student_grade_radar(
        StudentGrade.query.filter_by(ID=grade_id).first()).dump_options_with_quotes()


@app.route('/charts/test_grade_distributed_chart/<int:test_time>/<string:subject>')
def grade_distributed_chart(test_time: int, subject: str):
    return test_grade_distributed_chart(test_time, subject).dump_options_with_quotes()


@app.route('/charts/test_grade_avg_compare_chart/<int:test_time>')
def grade_avg_compare_chart(test_time: int):
    data = test_avg_grade_compare(test_time)
    result = {}
    for key, value in data.items():
        result[key] = json.loads(value.dump_options())
    return json.dumps(result)


@app.route('/charts/test_student_distributed_chart/<int:test_time>')
def student_distributed_chart(test_time: int):
    return test_student_distributed(test_time).dump_options_with_quotes()


@app.route('/charts/test_high_grade_distributed_chart/<int:test_time>')
def high_grade_distributed_chart(test_time: int):
    return test_high_grade_distributed(test_time).dump_options_with_quotes()
