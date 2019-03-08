from ..Models import db
from ..Models.User import User

roles_users = db.Table(
    'roles_users',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
)


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
    def has_role(user_id, item_type, item_id, name):
        return (db.session.query(Role.id).join(Role.users).filter(Role.item_type == item_type,
                                                                     Role.item_id == item_id,
                                                                     Role.name == name,
                                                                     User.id == user_id).scalar() is not None)

    @staticmethod
    def get_roles(user_id, item_type, name=None):
        if name is None:
            return Role.query.join(Role.users).filter(Role.item_type == item_type,
                                                      User.id == user_id).all()

        return Role.query.join(Role.users).filter(Role.item_type == item_type,
                                                  Role.name == name,
                                                  User.id == user_id).all()

    @staticmethod
    def delete(item_type, item_id):
        return Role.query.filter_by(item_type=item_type, item_id=item_id).delete()
