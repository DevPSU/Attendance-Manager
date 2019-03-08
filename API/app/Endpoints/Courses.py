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

    new_course, new_schedule = course_validator(request.get_json())
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


def course_validator(data, course=None):
    name = data.get('name')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    days_of_week = data.get('days_of_week')

    # If we are creating a new course, we must have all this info
    if course is None:
        if name is None or start_date is None or end_date is None or start_time is None or end_time is None or days_of_week is None:
            return error_json("Your request is missing information.", 400)
    else:
        schedule = course.schedules[0]

    if name is not None and not (2 < len(name) < 64):
        return error_json("You must enter a valid course name.", 400)


    # Make sure we have YYYY-MM-DD format
    if start_date is not None:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        except ValueError:
            return error_json("The start date is invalid (should be YYYY-MM-DD).", 400)

    if end_date is not None:
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return error_json("The end date is invalid (should be YYYY-MM-DD).", 400)

    # Make sure end date is after start date
    if course is None and start_date > end_date:
        return error_json("The end date must be after the start date.", 400)
    elif start_date is not None and end_date is not None and start_date > end_date:
        return error_json("The end date must be after the start date.", 400)
    elif start_date is None and end_date is not None and schedule.start_date > end_date:
        return error_json("The end date must be after the start date.", 400)
    elif start_date is not None and end_date is None and start_date > schedule.end_date:
        return error_json("The end date must be after the start date.", 400)

    # Make sure we have YYYY-MM-DD format
    if start_time is not None:
        try:
            start_time = datetime.strptime(start_time, '%H:%M:%S').time()
        except ValueError:
            return error_json("The start time is invalid (should be HH:MM:SS).", 400)

    if end_time is not None:
        try:
            end_time = datetime.strptime(end_time, '%H:%M:%S').time()
        except ValueError:
            return error_json("The end time is invalid (should be HH:MM:SS).", 400)

    # Make sure end time is after start time
    if course is None and start_time >= end_time:
        return error_json("The end date must be after the start date.", 400)
    elif start_time is not None and end_time is not None and start_time > end_time:
        return error_json("The end date must be after the start date.", 400)
    elif start_time is None and end_time is not None and schedule.start_time > end_time:
        return error_json("The end date must be after the start date.", 400)
    elif start_time is not None and end_time is None and start_time > schedule.end_time:
        return error_json("The end date must be after the start date.", 400)

    # Make sure days of week is array (list) of ALLOWED_DAYS_OF_WEEK
    if days_of_week is not None and not isinstance(days_of_week, list) or len(days_of_week) > 7:
        return error_json("The days of the week are invalid.", 400)
    if days_of_week is not None and any(day not in ALLOWED_DAYS_OF_WEEK for day in days_of_week):
        return error_json("The days of the week are invalid.", 400)
    days_of_week = '.'.join(days_of_week)

    if course is None:
        return Course(name=name), Schedule(type="weekly",
                                           start_date=start_date,
                                           end_date=end_date,
                                           start_time=start_time,
                                           end_time=end_time,
                                           days_of_week=days_of_week)

    if name is not None:
        course.name = name
    if start_date is not None:
        schedule.start_date = start_date
    if end_date is not None:
        schedule.end_date = end_date
    if start_time is not None:
        schedule.start_time = start_time
    if end_time is not None:
        schedule.end_time = end_time
    if days_of_week is not None:
        schedule.days_of_week = days_of_week

    return course, schedule


@courses.route("/", methods=["GET"])
@require_logged_in
def my_courses():
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


@courses.route("/<course_id>", methods=["PUT"])
@require_logged_in
def edit_course(course_id):
    user = request.user

    # HARD-CODED: Must be a 'Professor' role to edit a course
    if not Role.has_role(user.id, 'courses', course_id, 'Professor'):
        return error_json("You are unauthorized to make this request.", 401)

    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return error_json("Couldn't find that course.", 404)

    course, schedule = course_validator(request.get_json(), course=course)
    if not isinstance(course, Course):
        return course
    db.session.commit()
    role = Role.get_role(user.id, 'courses', course_id, 'Professor')

    json = course.to_dict(role=role, schedule=schedule)

    return jsonify(json), 200


@courses.route("/<course_id>", methods=["DELETE"])
@require_logged_in
def delete_course(course_id):
    user = request.user

    # HARD-CODED: Must be a 'Professor' role to delete a course
    if not Role.has_role(user.id, 'courses', course_id, 'Professor'):
        return error_json("You are unauthorized to make this request.", 401)

    # Delete roles associated with course since roles are polymorphic
    Role.delete('courses', course_id)
    # Delete course itself (automatically deletes schedules using cascading)
    Course.query.filter_by(id=course_id).delete()

    db.session.commit()

    json = {"deleted": 1}

    return jsonify(json), 200
