from ..Models import db

roles_users = db.Table(
    'roles_users',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)


# Creating the role table
class Role(db.Model):
    __tablename__ = 'roles'
    # Creating the columns of the roles table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, server_default='')
    item_id = db.Column(db.Integer)
    item_type = db.Column(db.String)
    users = db.relationship('User', secondary=roles_users, backref=db.backref('roles', lazy='dynamic'))
    created_at = db.Column(db.DateTime, default=db.func.now())
    modified_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, name=None):
        if name is not None:
            self.name = name
