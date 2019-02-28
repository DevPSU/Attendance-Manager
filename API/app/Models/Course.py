from ..Models import db


# Creating the courses table
class Course(db.Model):
    __tablename__ = 'courses'
    # Creating the columns of the course table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, server_default='')
    schedules = db.relationship('Schedule', backref='course', lazy=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    modified_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, name=None):
        if name is not None:
            self.name = name

    def to_dict(self, role=None, schedule=None):
        course_dict = {
            "id": self.id,
            "name": self.name,
            "created_at": str(self.created_at),
            "modified_at": str(self.modified_at)
        }

        if role is not None:
            course_dict['role'] = role.name
            # Adds schedule and role information to dict

        if schedule is not None:
            course_dict.update(schedule.to_dict())

        return course_dict
