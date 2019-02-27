from ..Models import db
import os
import binascii


# Creating the user table
class Course(db.Model):
    __tablename__ = 'courses'
    # Creating the columns of the course table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, server_default='')
    start_date = db.Column(db.Date, nullable=False, server_default='')
    end_date = db.Column(db.Date, nullable=False, server_default='')
    start_time = db.Column(db.Time, nullable=False, server_default='')
    end_time = db.Column(db.Time, nullable=False, server_default='')
    days_of_week = db.Column(db.String(18), nullable=False, server_default='')
    created_at = db.Column(db.DateTime, default=db.func.now())
    modified_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, name=None, start_date=None, end_date=None, start_time=None, end_time=None, days_of_week=None):
        if name is not None:
            self.name = name

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
