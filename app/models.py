from LoadData.DataModels import *


class AnalysisStudent(db.Model):
    __tablename__ = 'analysis_students'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # level:
    #     high: first 25%
    #     medium : top 25%-60%
    #     low : last 40%
    level = db.Column(db.String(8))
