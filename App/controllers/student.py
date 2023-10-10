from App.models import Student
from App.database import db
from App.config import config
import json

# Creates a new student
def create_student(name, faculty, degree):
    student = Student(name, faculty, degree)
    db.session.add(student)
    db.session.commit()
    return student

# Updates a desired student data
def update_student(id, name, degree, faculty):
    student = Student.query.filter_by(id=id).first()
    student.name = name
    student.degree = degree
    student.faculty = faculty
    db.session.commit()
    return student

# Deletes a student
def delete_student(id):
    student = Student.query.filter_by(id=id).first()
    db.session.delete(student)
    db.session.commit()

# Returns the desired student given their id
def get_student_by_id(id):
    return Student.query.filter_by(id=id).first()

# Returns the desired student given their id
def get_student_by_name(name):
    return Student.query.filter_by(name=name).all()

# Returns all students
def get_all_students():
    return Student.query.all()

# Return all students as a JSON object
def get_all_students_json():
    students = get_all_students()
    return json.dumps([student.toJSON() for student in students])

# Returns the desired student by given their id
def get_student_json(id):
    student = get_student_by_id(id)
    return json.dumps(student.toJSON())
