from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError


from.index import index_views

from App.controllers import (
    create_user,
    jwt_authenticate, 
    get_all_users,
    get_all_users_json,
    get_user_by_username,
    jwt_required
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

#Register a new user
@user_views.route('/users', methods=['POST'])
def register_user():
    data = request.json
    username = data['username']
    password = data['password']
    try:
        create_user(username, password)
        return jsonify({'message': f"user {username} created"})
    except IntegrityError:
        return jsonify({'message': f"username {username} already exists"}), 409
  
@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')