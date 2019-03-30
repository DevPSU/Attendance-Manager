from flask import Blueprint, request, jsonify

from ..Models import db
from ..Models.User import User
from ..Models.Course import Course
from ..Models.Schedule import Schedule
from ..Models.Role import Role, RoleName
from ..app import error_json
from .Auth import require_logged_in

from datetime import datetime
import string
import random

courses = Blueprint('courses', __name__, url_prefix="/courses")

ALLOWED_DAYS_OF_WEEK = ['M', 'TU', 'W', 'TH', 'F', 'SA', 'SU']


@courses.route("/join", methods=["POST"])
@require_logged_in
def join_course():
    data = request.get_json()
    user = request.user
    enrollment_code = data.get('enrollment_code')

    if enrollment_code is None:
        return error_json("Your request is missing information.", 400)
    if len(enrollment_code) != 8 or not enrollment_code.isalnum():
        return error_json("Your enrollment code is invalid.", 422)
    enrollment_code = enrollment_code.upper()

    course = Course.query.filter_by(enrollment_code=enrollment_code).first()
    if course is None:
        return error_json("Your enrollment code is invalid.", 422)

    if Role.get_by_user(course.id, user.id) is not None:
        error = "You are already in this course."
        return jsonify({'error': error}), 422

    # Add the user as a student automatically
    role_name = RoleName.STUDENT
    Role.set(course.id, user, role_name)

    json = course.to_dict(role_name=role_name, schedule=course.schedules[0])

    return jsonify(json), 200


@courses.route("/", methods=["POST"])
@require_logged_in
def create_course():
    user = request.user

    new_course, new_schedule = course_validator(request.get_json())
    if not isinstance(new_course, Course):
        return new_course

    # Generate a unique course enrollment code
    while True:
        enrollment_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        if Course.query.filter_by(enrollment_code=enrollment_code).scalar() is None:
            break
    new_course.enrollment_code = enrollment_code

    db.session.add(new_course)
    db.session.commit()

    # Add schedule for course
    new_schedule.course_id = new_course.id
    db.session.add(new_schedule)
    db.session.commit()

    # Automatically create roles for course
    Role.initialize(new_course.id)
    # Add user as professor of course
    role_name = RoleName.PROFESSOR
    Role.set(new_course.id, user, role_name)

    json = new_course.to_dict(role_name=role_name, schedule=new_schedule)

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

    # Get all of the user's roles in in all courses
    roles = Role.get_all_by_user(user.id)

    json = {'count': len(roles)}
    if len(roles) > 0:
        course_ids = [role.course_id for role in roles]
        courses = Course.query.filter(Course.id.in_(course_ids)).all()

        my_courses = []
        for i in range(len(courses)):
            role = roles[i]
            course = courses[i]
            course = course.to_dict(role_name=role.name, schedule=course.schedules[0])

            my_courses.append(course)

        json['courses'] = my_courses
    return jsonify(json), 200


@courses.route("/<course_id>", methods=["GET"])
@require_logged_in
def view_course(course_id):
    user = request.user

    role = Role.get_by_user(course_id, user.id)
    # Check if they are even in the course
    if role is None:
        return error_json("You are unauthorized to make this request.", 401)
    course = Course.query.filter_by(id=course_id).first()
    schedule = course.schedules[0]

    json = course.to_dict(role_name=role.name, schedule=schedule)

    return jsonify(json), 200


@courses.route("/<course_id>", methods=["PUT"])
@Role.requires(RoleName.PROFESSOR) # HARD-CODED: Must be a 'Professor' role to edit a course
@require_logged_in
def edit_course(course_id):
    user = request.user

    if not Role.has(course_id, user.id, RoleName.PROFESSOR):
        return error_json("You are unauthorized to make this request.", 401)

    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return error_json("Couldn't find that course.", 404)

    course, schedule = course_validator(request.get_json(), course=course)
    # If there was an error, 'course' will be the error_json package.
    if not isinstance(course, Course):
        return course
    db.session.commit()
    role = Role.get_by_user(course_id, user.id)

    json = course.to_dict(role_name=role.name, schedule=schedule)

    return jsonify(json), 200


@courses.route("/<course_id>", methods=["DELETE"])
@Role.requires(RoleName.PROFESSOR) # HARD-CODED: Must be a 'Professor' role to delete a course
@require_logged_in
def delete_course(course_id):
    # Delete all roles associated with the course
    Role.delete_all(course_id)
    # Delete course itself (automatically deletes schedules using cascading)
    Course.query.filter_by(id=course_id).delete()

    db.session.commit()

    json = {"deleted": 1}

    return jsonify(json), 200
