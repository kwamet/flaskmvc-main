from App.models import Review, Student, User
from App.database import db

def create_review(studentId, rating, comment, userId):
    if studentId:
        review = Review(studentId, rating, comment, userId)
        db.session.add(review)
        db.session.commit()
        return review
    return None

def update_review(id, studentId, rating, comment, userId):
    review = Review.query.filter_by(id=id).first()
    if review is None:
        return None
    review.rating = rating
    review.comment = comment
    db.session.commit()
    return review

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

def get_reviews_by_student(studentId):
    if studentId:
        return Review.query.filter_by(studentId=studentId).all()
    return None

def get_reviews_by_user(userId):
    if userId:
        return Review.query.filter_by(userId=userId).all()
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

