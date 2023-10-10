from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from .index import index_views

from App.controllers import (
    create_review,
    update_review,
    delete_review,
    get_all_reviews,
)

review_views = Blueprint('review_views', __name__, template_folder='../templates')

# Create a new review and add it to the database
@review_views.route("/api/reviews", methods=["POST"])
@jwt_required()
def create_review_endpoint():
    data = request.json
    current_user = jwt_current_user
    review = create_review(data['student_id'], data['rating'], data['comment'], current_user.id)
    return jsonify(message="Review created", review=review.toJSON())
