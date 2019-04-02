from flask import Blueprint, request, jsonify

from ..app import error_json

from ..Models.User import User
from ..Models.Role import Role, RoleName
from .Auth import require_logged_in

courses_users = Blueprint('courses_users', __name__, url_prefix="/courses/<course_id>/users")

@courses_users.route("/", methods=["GET"])
@require_logged_in
@Role.requires([RoleName.PROFESSOR, RoleName.TA]) # HARD-CODED: Must be a Professor or TA
def view_users_in_course(course_id):
    # Get all of the users in the course
    roles_users = Role.get_all_roles_users(course_id)

    json = {'count': len(roles_users)}
    if len(roles_users) > 0:
        my_users = []
        for i in range(len(roles_users)):
            role = roles_users[i][0]
            user = roles_users[i][1]
            user = user.to_dict(role_name=role.name)

            my_users.append(user)

        json['users'] = my_users

    return jsonify(json), 200


@courses_users.route("/<user_id>", methods=["GET"])
@require_logged_in
def view_user_in_course(course_id, user_id):
    user = request.user

    # HARD-CODED: Check if the user is a professor, TA, or trying to access their own data
    if user_id != user.id:
        if not Role.has_any(course_id, user.id, [RoleName.PROFESSOR, RoleName.TA]):
            return error_json("You are unauthorized to make this request.", 401)

    role = Role.get_by_user(course_id, user_id)
    if role is None:
        return error_json("You aren't in this course.", 422)

    me = User.query.filter_by(id=user_id).first()

    return jsonify(me.to_dict(role_name=role.name)), 200


@courses_users.route("/<user_id>", methods=["PUT"])
@require_logged_in
@Role.requires(RoleName.PROFESSOR) # HARD-CODED: Only professors can edit roles
def edit_user_in_course(course_id, user_id):
    data = request.get_json()
    role_name = data.get('role')

    if role_name is None:
        return error_json("Your request is missing information.", 400)

    # Get the list of available roles
    available_roles = set(role_name.value for role_name in RoleName)
    role_name = role_name.title()
    if role_name not in available_roles:
        return error_json("You must request a valid role.", 422)

    # Don't do anything if their role isn't changing
    old_role = Role.get_by_user(course_id, user_id)
    if old_role.name == role_name:
        me = User.query.filter_by(id=user_id).first()
        return jsonify(me.to_dict(role_name=old_role.name)), 200

    # Don't change a professor's role if they are the only professor
    professor_role = RoleName.PROFESSOR.value
    if old_role.name == professor_role and Role.count_by_name(course_id, professor_role) < 2:
        return error_json("There must be at least 1 professor in the course.", 422)

    me = User.query.filter_by(id=user_id).first()
    role = Role.set(course_id, me, role_name)

    return jsonify(me.to_dict(role_name=role.name)), 200


@courses_users.route("/<user_id>", methods=["DELETE"])
@require_logged_in
def remove_user_from_course(course_id, user_id):
    user = request.user

    # HARD-CODED: Check if the user is a professor or trying to remove themselves
    if user_id != user.id:
        if not Role.has(course_id, user.id, RoleName.PROFESSOR):
            return error_json("You are unauthorized to make this request.", 401)

    # Make sure we aren't removing a professor
    if Role.has(course_id, user_id, RoleName.PROFESSOR):
        return error_json("You cannot remove professors.", 401)

    # Remove the user's access to the course
    me = User.query.filter_by(id=user_id).first()
    Role.remove_user(course_id, me)

    json = {"removed": 1}

    return jsonify(json), 200
