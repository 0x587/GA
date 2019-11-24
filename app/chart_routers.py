from app import app
from AnalysisData.Class import class_history_grade, class_grade_distributed
from AnalysisData.Student.charts import student_grade_radar, student_grade_compared
from app.models import *


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
