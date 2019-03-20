from ..Models import db
from ..Models.User import User

from enum import Enum


roles_users = db.Table(
    'roles_users',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
)


class RoleName(Enum):
    PROFESSOR = "Professor"
    STUDENT = "Student"

# Creating the role table
class Role(db.Model):
    __tablename__ = 'roles'
    # Creating the columns of the roles table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, server_default='')
    item_id = db.Column(db.Integer)
    item_type = db.Column(db.String)
    users = db.relationship('User',
                            secondary=roles_users,
                            backref=db.backref('roles', passive_deletes=True, lazy='dynamic'))
    created_at = db.Column(db.DateTime, default=db.func.now())
    modified_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    def __init__(self, name=None):
        if name is not None:
            self.name = name

    @staticmethod
    def create_role(user, item, name):
        if isinstance(name, Enum):
            name = name.value

        role = Role(name=name)
        role.item_id = item.id
        role.item_type = item.__tablename__
        role.users.append(user)

        db.session.add(role)
        db.session.commit()

        return role


    @staticmethod
    def set_role(user, item, name):
        role = Role.get_role(user.id, item.__tablename__, item.id)

        if role is None:
            Role.create_role(user, item, name)
        else:
            role.name = name
            db.session.commit()

        return role


    @staticmethod
    def has_role(user_id, item_type, item_id, name):
        if isinstance(name, Enum):
            name = name.value

        return (db.session.query(Role.id).join(Role.users).filter(Role.item_type == item_type,
                                                                     Role.item_id == item_id,
                                                                     Role.name == name,
                                                                     User.id == user_id).scalar() is not None)

    @staticmethod
    def get_role(user_id, item_type, item_id):
        return Role.query.join(Role.users).filter(Role.item_type == item_type,
                                                  Role.item_id == item_id,
                                                  User.id == user_id).first()
    @staticmethod
    def get_roles(user_id, item_type, name=None):
        if isinstance(name, Enum):
            name = name.value

        if name is None:
            return Role.query.join(Role.users).filter(Role.item_type == item_type,
                                                      User.id == user_id).all()

        return Role.query.join(Role.users).filter(Role.item_type == item_type,
                                                  Role.name == name,
                                                  User.id == user_id).all()

    @staticmethod
    def delete(item_type, item_id):
        return Role.query.filter_by(item_type=item_type, item_id=item_id).delete()
