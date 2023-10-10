from App.database import db
from datetime import datetime

class Review(db.Model):
    __tablename__ = 'review'
    reviewId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(10), db.ForeignKey('user.id'), nullable=False)
    student_id = db.Column(db.String(10), db.ForeignKey('student.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    up_votes = db.Column(db.Integer, nullable=False, default=0)
    down_votes = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, user_id, student_id, rating, comment):
        self.user_id = user_id
        self.student_id = student_id
        self.rating = rating
        self.comment = comment
        self.up_votes = 0
        self.down_votes = 0

    def toJSON(self):
        return {
            'reviewId': self.reviewId,
            'user_id': self.user_id,
            'student_id': self.student_id,
            'rating': self.rating,
            'comment': self.comment,
            'date': self.date,
            'up_votes': self.up_votes,
            'down_votes': self.down_votes
        }
        