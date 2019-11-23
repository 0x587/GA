from app import app
from AnalysisData.Class import class_history_grade


@app.route('/charts/history_grade_chart/<int:class_index>')
def history_grade_chart(class_index: int):
    return class_history_grade(
        class_index).dump_options_with_quotes()
