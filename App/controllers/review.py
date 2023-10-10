from App.models import Review, Student, User
from App.database import db

def create_review(student_id, rating, comment, user_id):
    if student_id == Student.query.filter_by(id=student_id).first().id:
        review =  Review(user_id, student_id, rating, comment)  
        db.session.commit()
        return review
    return None

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

def delete_review(id):
    review = Review.query.filter_by(id=id).first()
    if review is None:
        return None
    db.session.delete(review)
    db.session.commit()
    return review

def get_review(id):
    return Review.query.filter_by(id=id).first()
    if review is None:
        return None
    return review.toJSON()

def get_all_reviews():
    return Review.query.all()

def get_reviews_by_student(student_id):
    if student_id:
        return Review.query.filter_by(student_id=student_id).all()
    return None

def get_reviews_by_user(user_id):
    if user_id:
        return Review.query.filter_by(user_id=user_id).all()
    return None
    
def upvote_review(id):
    review = Review.query.filter_by(id=id).first()
    if review is None:
        return None
    review.upvotes += 1
    db.session.commit()
    return review

def downvote_review(id):
    review = Review.query.filter_by(id=id).first()
    if review is None:
        return None
    review.downvotes += 1
    db.session.commit()
    return review

