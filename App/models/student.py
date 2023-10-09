from App.database import db

class Student(db.Model):
    studentId = db.Column(db.String(10), primary_key=True)
    studentName = db.Column(db.String(50), nullable=False)
    karma = db.Column(db.Integer, nullable=False)
    reviews = db.relationship('Review', backref='student', lazy=True)

   def calculate_karma(self):
       self.karma = 0
       for review in self.reviews:
           self.karma += review.rating
       return self.karma
    
    def toJSON(self):
        return {
            'studentId': self.studentId,
            'studentName': self.studentName,
            'karma': self.karma
            'reviews': self.reviews
        }