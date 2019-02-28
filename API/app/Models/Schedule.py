from ..Models import db


# Creating the schedule table
class Schedule(db.Model):
    __tablename__ = 'schedules'
    # Creating the columns of the schedule table
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    type = db.Column(db.String, nullable=False, default="weekly")
    start_date = db.Column(db.Date, nullable=False, server_default='')
    end_date = db.Column(db.Date, nullable=False, server_default='')
    start_time = db.Column(db.Time, nullable=False, server_default='')
    end_time = db.Column(db.Time, nullable=False, server_default='')
    days_of_week = db.Column(db.String(18), nullable=False, server_default='')
    created_at = db.Column(db.DateTime, default=db.func.now())
    modified_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, type=None, course_id=None, start_date=None, end_date=None, start_time=None, end_time=None, days_of_week=None):
        if type is not None:
            self.type = type
        if course_id is not None:
            self.course_id = course_id

        if start_date is not None:
            self.start_date = start_date

        if end_date is not None:
            self.end_date = end_date

        if start_time is not None:
            self.start_time = start_time

        if end_time is not None:
            self.end_time = end_time

        if days_of_week is not None:
            self.days_of_week = days_of_week

    def to_dict(self):
        return {
            "start_date": str(self.start_date),
            "end_date": str(self.end_date),
            "start_time": str(self.start_time),
            "end_time": str(self.end_time),
            "days_of_week": self.days_of_week.split('.')
        }
