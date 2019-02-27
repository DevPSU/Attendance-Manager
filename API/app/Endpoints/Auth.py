from functools import wraps
from flask import Blueprint, request, jsonify
from sqlalchemy import or_

from ..Models import db
from ..Models.User import User
from ..app import application, error_json, bcrypt

from datetime import datetime, timedelta
import re
import jwt


auth = Blueprint('auth', __name__, url_prefix="/auth")


# Verify that the user secret key is valid
def require_logged_in(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return error_json("You must include a valid token with this request.", 400)

        bearer_token_match = re.match('^Bearer\s+(.*)', auth_header.strip())
        if not bearer_token_match:
            return error_json("You must include a valid token with this request.", 401)

        bearer_token = bearer_token_match.group(1)

        try:
            jwt_data = jwt.decode(bearer_token.encode(), application.secret_key, algorithms='HS256')
        except jwt.DecodeError:
            return error_json("Your bearer token is invalid.", 401)

        user = User.query.filter(User.id == jwt_data['id'],
                                 User.secret_key == jwt_data['key'],
                                 or_(User.expires_at > datetime.now(), User.expires_at == None)).first()
        if user is None:
            return error_json("You are unauthorized to make this request.", 401)

        request.user = user

        return func(*args, **kwargs)
    return decorated_function


@auth.route("/verify", methods=["POST"])
@require_logged_in
def verify_account():
    user = request.user

    json = {
        "user_id": user.id
    }

    return jsonify(json), 200


@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email', '')
    password = data.get('password')
    should_expire = data.get('should_expire')

    # Verify first name, last name, email, and password are not missing
    if first_name is None or last_name is None or email is None or password is None:
        return error_json("You must enter a first name, last name, email, and password.", 400)

    # Verify length of the first name
    if len(first_name) > 64:
        return error_json("Your first name cannot be more than 64 characters.", 422)

    # Verify length of the first name
    if len(last_name) > 64:
        return error_json("Your last name cannot be more than 64 characters.", 422)

    # Verify length of the password
    if len(password) > 64:
        return error_json("Your password cannot be more than 64 characters.", 422)

    # Verify email address is valid format
    if not re.match(r"^[^\s@]+@([^\s@.,]+\.)+[^\s@.,]{2,}$", email):
        return error_json("That email address looks invalid.", 422)

    # Verify email address is unique
    if User.query.filter_by(email=email).scalar() is not None:
        return error_json("Your email address is already in use.", 422)

    password_hash = bcrypt.generate_password_hash(password, rounds=13).decode('utf-8')
    # Erase plaintext password for security
    del password

    new_user = User(first_name=first_name, last_name=last_name, email=email, password_hash=password_hash)

    if should_expire is None or should_expire == 1:
        new_user.expires_at = datetime.now() + timedelta(minutes=30)

    db.session.add(new_user)
    db.session.commit()

    bearer_token = jwt.encode({'id': new_user.id, 'key': new_user.secret_key}, application.secret_key, algorithm='HS256')
    bearer_token = bearer_token.decode()

    json = {
        "id": new_user.id,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "email": new_user.email,
        "bearer_token": bearer_token,
        "created_at": str(new_user.created_at)
    }
    if new_user.expires_at is not None:
        json["expires_at"] = str(new_user.expires_at)

    return jsonify(json), 200


@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get('email', '')
    password = data.get('password')
    should_expire = data.get('should_expire')

    # Verify email and password are not missing
    if email is None or password is None:
        return error_json("You must enter an email and password.", 400)

    # Verify length of the password
    if len(password) > 64:
        return error_json("Your password cannot be more than 64 characters.", 422)

    # Verify email address is valid format
    if not re.match(r"^[^\s@]+@([^\s@.,]+\.)+[^\s@.,]{2,}$", email):
        return error_json("That email address looks invalid.", 422)

    user = User.query.filter_by(email=email).first()

    if user is None or not bcrypt.check_password_hash(user.password_hash, password):
        return error_json("Your email and password do not match.", 401)

    user.secret_key = User.generate_key(128)
    user.expires_at = None
    if should_expire is None or should_expire == 1:
        user.expires_at = datetime.now() + timedelta(minutes=30)
    db.session.commit()

    bearer_token = jwt.encode({'id': user.id, 'key': user.secret_key}, application.secret_key, algorithm='HS256')
    bearer_token = bearer_token.decode()

    json = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "bearer_token": bearer_token
    }
    if user.expires_at is not None:
        json["expires_at"] = str(user.expires_at)

    return jsonify(json), 200


@auth.route("/health_check", methods=["get"])
def health_check():

    json = {
        "health": "OK"
    }

    return jsonify(json), 200
