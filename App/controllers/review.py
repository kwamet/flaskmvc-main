from App.models import Review, Student, User
from App.database import db

# Creates a student review for the desired student
def create_review(student_id, rating, comment, user_id):
    if student_id == Student.query.filter_by(id=student_id).first().id:
        review =  Review(user_id, student_id, rating, comment)  
        db.session.commit()
        return review
    return None

# Updates the desired student review
def update_review(id, student_id, rating, comment, user_id):
    if user_id==Review.query.filter_by(id=id).first().user_id:
        review = Review.query.filter_by(id=id).first()
        if review is None:
            return None
        review.rating = rating
        review.comment = comment
        db.session.commit()
        return review
    return None

# Deletes the desired review
def delete_review(id):
    review = Review.query.filter_by(id=id).first()
    if review is None:
        return None
    db.session.delete(review)
    db.session.commit()
    return review

# Returns the desired review gievn its ID
def get_review(id):
    return Review.query.filter_by(id=id).first()
    if review is None:
        return None
    return review.toJSON()

# Returns all reviews
def get_all_reviews():
    return Review.query.all()

# Returns all reviews of a student given their student_id
def get_reviews_by_student(student_id):
    if student_id:
        return Review.query.filter_by(student_id=student_id).all()
    return None

# Returns all reviews made by a user given their user_id
def get_reviews_by_user(user_id):
    if user_id:
        return Review.query.filter_by(user_id=user_id).all()
    return None

# Upvotes a review
def upvote_review(id):
    review = Review.query.filter_by(id=id).first()
    if review is None:
        return None
    review.upvotes += 1
    db.session.commit()
    return review

# Downvotes a review
def downvote_review(id):
    review = Review.query.filter_by(id=id).first()
    if review is None:
        return None
    review.downvotes += 1
    db.session.commit()
    return review
