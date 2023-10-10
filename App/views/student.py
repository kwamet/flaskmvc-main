from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required


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

@student_views.route("/api/students", methods=["POST"])
def create_student_endpoint():
    data = request.json
    student= create_student(name=data['name'], faculty=data['faculty'] , degree=data['degree'])
    return jsonify({'message': f"student {data['name']} created"})

@student_views.route("/api/students", methods=["GET"])
def test():
    test = "Hello World"
    return jsonify({'message': test})
