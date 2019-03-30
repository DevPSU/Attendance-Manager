from flask import Blueprint, request, jsonify

from ..Models import db
from ..Models.User import User
from .Auth import require_logged_in

courses_users = Blueprint('courses_users', __name__, url_prefix="/courses/<course_id>/users")
'''
@courses_users.route("/", methods=["GET"])
@require_logged_in
def users_in_course(course_id):
    user = request.user

    # Get all of our user roles for the courses table
    roles = Role.get_roles(user.id, 'courses')

    json = {'count': len(roles)}
    if len(roles) > 0:
        course_ids = [role.item_id for role in roles]
        courses = Course.query.filter(Course.id.in_(course_ids)).all()

        my_courses = []
        for i in range(len(courses)):
            role = roles[i]
            course = courses[i]
            course = course.to_dict(role=role, schedule=course.schedules[0])

            my_courses.append(course)

        json['courses'] = my_courses
    return jsonify(json), 200
'''
