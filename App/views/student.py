from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required
from urllib.parse import unquote

from.index import index_views

from App.controllers import (
    create_student,
    update_student,
    delete_student,
    get_student_by_id,
    get_student_by_name,
    get_all_students,
    get_all_students_json,
    get_student_json
)


student_views = Blueprint('student_views', __name__, template_folder='../templates')

# Create a new student and add it to the database
@student_views.route("/api/students", methods=["POST"])
def create_student_endpoint():
    data = request.json
    student = create_student(data['name'], data['faculty'], data['degree'])
    return jsonify(message="Student created", student=student.toJSON())


# Update a student in the database by id    
@student_views.route("/api/students/<int:student_id>/edit", methods=["PUT"])
def update_student_endpoint(student_id):
    if get_student_by_id(student_id) is None:
        return jsonify(message="Student not found"), 404
    data = request.json
    student = update_student(student_id, data['name'], data['faculty'], data['degree'])
    return jsonify(message="Student updated", student=student.toJSON())

#Delete a student from the database by id
@student_views.route("/api/students/<int:student_id>", methods=["DELETE"])
def delete_student_endpoint(student_id):
    if get_student_by_id(student_id) is None:
        return jsonify(message="Student not found"), 404
    delete_student(student_id)
    return jsonify(message="Student deleted")

# Get a student from the database by id
@student_views.route("/api/students/<int:student_id>", methods=["GET"])
def get_student_by_id_endpoint(student_id):
    student = get_student_by_id(student_id)
    if student is None:
        return jsonify(message="Student not found"), 404
    return jsonify(student=student.toJSON())

# Get a student from the database by name
@student_views.route('/api/students/<path:student_name>', methods=['GET'])
def get_student_by_name_endpoint(student_name):
    student_name = unquote(student_name)
    students = get_student_by_name(student_name)
    if students is None:
        return jsonify(message="Student not found"), 404
    # Convert each student in the list to JSON
    student_json_list = [student.toJSON() for student in students]
    return jsonify(students=student_json_list)


# Get all students from the database
@student_views.route("/api/students", methods=["GET"])
def get_all_students_endpoint():
    students = get_all_students()
    if students:
        student_json_list = [student.toJSON() for student in students]
        return jsonify(students=student_json_list)
    return jsonify(message="No students found"), 404

# Get reviews for a student from the database by id
@student_views.route("/api/students/<int:student_id>/reviews", methods=["GET"])
def get_reviews_by_student_endpoint(student_id):
    student = get_student_by_id(student_id)
    if student is None:
        return jsonify(message="Student not found"), 404
    reviews = student.reviews
    if reviews:
        review_json_list = [review.toJSON() for review in reviews]
        return jsonify(reviews=review_json_list)
    return jsonify(message="No reviews found"), 404
    