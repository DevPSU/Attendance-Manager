from ..Models import db
from ..Models.User import User

from flask import request
from sqlalchemy import func
from ..app import error_json

from enum import Enum
from functools import wraps

roles_users = db.Table(
    'roles_users',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
)


class RoleName(Enum):
    PROFESSOR = "Professor"
    TA = "Teaching Assistant"
    STUDENT = "Student"


# Creating the role table
class Role(db.Model):
    __tablename__ = 'roles'
    # Creating the columns of the roles table
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(64), nullable=False, server_default='')
    users = db.relationship('User',
                            secondary=roles_users,
                            backref=db.backref('roles', passive_deletes=True, lazy='dynamic'))
    created_at = db.Column(db.DateTime, default=db.func.now())
    modified_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, course_id=None, name=None):
        if course_id is not None:
            self.course_id = course_id
        if name is not None:
            self.name = name

    @staticmethod
    def initialize(course_id):
        for name in RoleName:
            name = name.value
            role = Role(course_id=course_id, name=name)

            db.session.add(role)

        db.session.commit()

    @staticmethod
    def set(course_id, user, name):
        if isinstance(name, Enum):
            name = name.value

        # Check if the user already has a role for this course
        role = Role.get_by_user(course_id, user.id)

        if role is None:
            # Find the role and add the user to it
            role = Role.get_by_name(course_id, name)
            role.users.append(user)
        else:
            # Remove the old role and add a new one
            role.users.remove(user)

            role = Role.get_by_name(course_id, name)
            role.users.append(user)

        db.session.commit()

        return role

    @staticmethod
    def has(course_id, user_id, name):
        if isinstance(name, Enum):
            name = name.value

        return (db.session.query(Role.id).join(Role.users).filter(Role.course_id == course_id,
                                                                     Role.name == name,
                                                                     User.id == user_id).scalar() is not None)

    @staticmethod
    def has_any(course_id, user_id, names):
        role_names = []
        for i in range(len(names)):
            name = names[i]
            if isinstance(name, Enum):
                role_names.append(name.value)
            else:
                role_names.append(name)

        return (db.session.query(Role.id).join(Role.users).filter(Role.course_id == course_id,
                                                                     Role.name.in_(role_names),
                                                                     User.id == user_id).scalar() is not None)

    @staticmethod
    def get_by_user(course_id, user_id):
        return Role.query.join(Role.users).filter(Role.course_id == course_id,
                                                  User.id == user_id).first()

    @staticmethod
    def get_by_name(course_id, name):
        return Role.query.filter_by(course_id=course_id, name=name).first()

    @staticmethod
    def count_by_name(course_id, name):
        if isinstance(name, Enum):
            name = name.value

        count = db.session.query(func.count(User.id)).join(User.roles).filter(Role.course_id == course_id,
                                                                             Role.name == name).scalar()
        print(count)
        return count

    @staticmethod
    def get_all_roles_users(course_id):
        return db.session.query(Role, User).filter(Role.course_id == course_id).join(Role.users).all()

    @staticmethod
    def get_all_by_user(user_id):
        return Role.query.join(Role.users).filter(User.id == user_id).all()

    @staticmethod
    def remove_user(course_id, user):
        role = Role.get_by_user(course_id, user.id)

        role.users.remove(user)
        db.session.commit()

        return True

    @staticmethod
    def delete_all(course_id):
        return Role.query.filter_by(course_id=course_id).delete()

    # Decorator for having a role
    @staticmethod
    def requires(role_name):
        def requires_wrapped(func):
            @wraps(func)
            def decorated_function(*args, **kwargs):
                course_id = kwargs['course_id']

                # If we have multiple role names
                if isinstance(role_name, list):
                    role_names = role_name
                    has_role = Role.has_any(course_id, request.user.id, role_names)
                else:
                    has_role = Role.has(course_id, request.user.id, role_name)

                if not has_role:
                    return error_json("You are unauthorized to make this request.", 401)

                return func(*args, **kwargs)

            return decorated_function

        return requires_wrapped

