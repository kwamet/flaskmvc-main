from App.database import db
from datetime import datetime

class Review(db.Model):
    reviewId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String(10), db.ForeignKey('user.userId'), nullable=False)
    studentId = db.Column(db.String(10), db.ForeignKey('student.studentId'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    upVotes = db.Column(db.Integer, nullable=False, default=0)
    downVotes = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, userId, studentId, rating, comment):
        self.userId = userId
        self.studentId = studentId
        self.rating = rating
        self.comment = comment
        self.upVotes = 0
        self.downVotes = 0

    def toJSON(self):
        return {
            'reviewId': self.reviewId,
            'userId': self.userId,
            'studentId': self.studentId,
            'rating': self.rating,
            'comment': self.comment,
            'date': self.date,
            'upVotes': self.upVotes,
            'downVotes': self.downVotes
        }
        