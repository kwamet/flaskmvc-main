from App.database import db

class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    faculty = db.Column(db.String(50), nullable=False)
    degree = db.Column(db.String(50), nullable=False)
    karma = db.Column(db.Integer, nullable=False)
    reviews = db.relationship('Review', backref='student', lazy=True)

    def __init__(self, name, faculty, degree):
        self.name = name
        self.faculty = faculty
        self.degree = degree
        self.karma = 0
        self.reviews = []

    def calculate_karma(self):
       self.karma = 0
       for review in self.reviews:
           self.karma += review.rating
       return self.karma
    
    def toJSON(self):
        return {
            'studentId': self.id,
            'studentName': self.name,
            'karma': self.calculate_karma(),
            'reviews': self.reviews
        }