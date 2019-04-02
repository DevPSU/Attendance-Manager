from ..Models import db
import os
import binascii

from enum import Enum

# Creating the user table
class User(db.Model):
    __tablename__ = 'users'
    # Creating the columns of the user table
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False, server_default='')
    last_name = db.Column(db.String(64), nullable=False, server_default='')
    email = db.Column(db.String(128), unique=True, nullable=False, server_default='')
    password_hash = db.Column(db.String(64), nullable=False, server_default='')
    secret_key = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=db.func.now())
    modified_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    expires_at = db.Column(db.DateTime)

    def __init__(self, first_name=None, last_name=None, email=None, password_hash=None):
        if first_name is not None:
            self.first_name = first_name

        if last_name is not None:
            self.last_name = last_name

        if email is not None:
            self.email = email

        if password_hash is not None:
            self.password_hash = password_hash

        self.secret_key = User.generate_key(64)

    def to_dict(self, role_name=None):
        user_dict = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }

        if role_name is not None:
            if isinstance(role_name, Enum):
                role_name = role_name.value

            user_dict['role'] = role_name
            # Adds schedule and role information to dict

        return user_dict

    @staticmethod
    def generate_key(length):
        return binascii.hexlify(os.urandom(length // 2)).decode()
