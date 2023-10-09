from App.models import Student
from App.database import db
from App.config import config
import requests
import json

def create_student(name=name, degree=degree, faculty=faculty):
    student = Student(name, degree, faculty)
    db.session.add(student)
    db.session.commit()
    return student

def update_student(id, name=name, degree=degree, faculty=faculty):
    student = Student.query.filter_by(id=id).first()
    student.name = name
    student.degree = degree
    student.faculty = faculty
    db.session.commit()
    return student

def delete_student(id):
    student = Student.query.filter_by(id=id).first()
    db.session.delete(student)
    db.session.commit()

def get_student_by_id(id):
    return Student.query.filter_by(id=id).first()

def get_student_by_name(name):
    return Student.query.filter_by(name=name).all()

def get_all_students():
    return Student.query.all()

def get_all_students_json():
    students = get_all_students()
    return json.dumps([student.toJSON() for student in students])

def get_student_json(id):
    student = get_student_by_id(id)
    return json.dumps(student.toJSON())
