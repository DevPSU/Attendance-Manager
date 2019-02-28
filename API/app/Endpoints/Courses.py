from flask import Blueprint, request, jsonify

from ..Models import db
from ..Models.User import User
from ..Models.Course import Course
from ..Models.Schedule import Schedule
from ..Models.Role import Role
from ..app import error_json
from .Auth import require_logged_in

from datetime import datetime

courses = Blueprint('courses', __name__, url_prefix="/courses")

ALLOWED_DAYS_OF_WEEK = ['M', 'TU', 'W', 'TH', 'F', 'SA', 'SU']


@courses.route("/", methods=["POST"])
@require_logged_in
def create_course():
    user = request.user

    new_course, new_schedule = create_course_validator(request.get_json())
    if not isinstance(new_course, Course):
        return new_course

    db.session.add(new_course)
    db.session.commit()

    # Add schedule for course
    new_schedule.course_id = new_course.id
    db.session.add(new_schedule)

    # Add user as professor of course
    new_role = Role(name="Professor")
    new_role.item_id = new_course.id
    new_role.item_type = new_course.__tablename__
    new_role.users.append(user)

    db.session.add(new_role)
    db.session.commit()

    json = new_course.to_dict(role=new_role, schedule=new_schedule)

    return jsonify(json), 200


def create_course_validator(data):
    name = data.get('name')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    days_of_week = data.get('days_of_week')

    if name is None or not (2 < len(name) < 64):
        return error_json("You must enter a valid course name.", 400)

    if start_date is None or end_date is None or start_time is None or end_time is None or days_of_week is None:
        return error_json("You must enter a start date and time, end date and time, and days of the week.", 400)

    # Make sure we have YYYY-MM-DD format
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return error_json("The start date or end date are formatted incorrectly (should be YYYY-MM-DD).", 400)

    # Make sure end date is after start date
    if start_date > end_date:
        return error_json("The end date must be after the start date.", 400)

    # Make sure we have HH:MM:SS format
    try:
        start_time = datetime.strptime(start_time, '%H:%M:%S').time()
        end_time = datetime.strptime(end_time, '%H:%M:%S').time()
    except ValueError:
        return error_json("The start time or end time are formatted incorrectly (should be HH:MM:SS).", 400)

    # Make sure end time is after start time
    if start_time >= end_time:
            return error_json("The end time must be after the start time.", 400)

    # Make sure days of week is array (list) of ALLOWED_DAYS_OF_WEEK
    if not isinstance(days_of_week, list) or len(days_of_week) > 7:
        return error_json("The days of the week are formatted incorrectly.", 400)
    if any(day not in ALLOWED_DAYS_OF_WEEK for day in days_of_week):
        return error_json("The days of the week are formatted incorrectly.", 400)
    days_of_week = '.'.join(days_of_week)

    return Course(name=name), Schedule(type="weekly",
                                       start_date=start_date,
                                       end_date=end_date,
                                       start_time=start_time,
                                       end_time=end_time,
                                       days_of_week=days_of_week)


@courses.route("/", methods=["GET"])
@require_logged_in
def my_courses():
    user = request.user

    my_courses_roles = db.session.query(Course, Role, Schedule).\
        join(User.roles).filter(Role.item_type == 'courses', User.id == user.id).all()

    json = {'count': len(my_courses_roles)}
    if len(my_courses_roles) > 0:
        my_courses_list = []
        for course_role in my_courses_roles:
            course, role, schedule = course_role

            course = course.to_dict(role=role, schedule=schedule)

            my_courses_list.append(course)

        json['courses'] = my_courses_list

    return jsonify(json), 200


@courses.route("/<course_id>", methods=["GET"])
@require_logged_in
def view_course(course_id):
    user = request.user

    course, schedule, role = db.session.query(Course, Schedule, Role).join(Role.users).filter(
        Role.item_type == 'courses',
        Role.item_id == course_id,
        User.id == user.id,
        Course.id == course_id
    ).first()

    if role is None:
        return error_json("You are unauthorized to make this request.", 401)

    json = course.to_dict(role=role, schedule=schedule)

    return jsonify(json), 200
