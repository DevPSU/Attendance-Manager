from ..Models import db

from enum import Enum

users_courses = db.Table(
    'users_courses',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE')),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'))
)


# Creating the courses table
class Course(db.Model):
    __tablename__ = 'courses'
    # Creating the columns of the course table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, server_default='')
    enrollment_code = db.Column(db.String(8))
    schedules = db.relationship('Schedule', passive_deletes=True, backref='course', lazy="joined")
    users = db.relationship('User',
                            secondary=users_courses,
                            backref=db.backref('courses', passive_deletes=True, lazy='dynamic'))
    roles = db.relationship('Role', passive_deletes=True, backref='course', lazy='dynamic')
    created_at = db.Column(db.DateTime, default=db.func.now())
    modified_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, name=None):
        if name is not None:
            self.name = name

    def to_dict(self, role_name=None, schedule=None):
        course_dict = {
            "id": self.id,
            "name": self.name,
            "enrollment_code": self.enrollment_code,
            "created_at": str(self.created_at),
            "modified_at": str(self.modified_at)
        }

        if role_name is not None:
            if isinstance(role_name, Enum):
                role_name = role_name.value

            course_dict['role'] = role_name
            # Adds schedule and role information to dict

        if schedule is not None:
            course_dict.update(schedule.to_dict())

        return course_dict
