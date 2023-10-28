import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User
from App.controllers.user import (
    create_user,
    get_user_by_username,
    get_user,
    get_all_users,
    get_all_users_json,
    update_user
)
from App.controllers.student import (
    create_student,
    update_student,
    delete_student,
    get_student_by_id
    get_student_by_name,
    get_all_students,
    get_all_students_json,
    get_student_json
)
from App.controllers.review import (
    create_review,
    update_review,
    delete_review,
    get_review,
    get_all_reviews,
    get_reviews_by_student
    get_reviews_by_user
    upvote_review,
    downvote_review
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = User("bob", "bobpass")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)

# Unit tests for Student model
class StudentUnitTests(unittest.TestCase):
    def test_new_student(self):
        student = Student("Kwame Trancoso", "Engineering", "Bachelor's")
        assert (
            student.name == "Kwame Trancoso"
            and student.faculty == "Engineering"
            and student.programme == "Bachelor's"
        )

    def test_student_to_json(self):
        student = Student("Kwame Trancoso", "Engineering", "Bachelor's")
        student_json = student.to_json()
        self.assertDictEqual(
            student_json,
            {
                "faculty": "Engineering",
                "id": None,
                "karma": 0,
                "name": "Kwame Trancoso",
                "degree": "Bachelor's",
            },
        )

    def test_student_karma(self):
        with self.subTest("No reviews"):
            student = Student("Kwame Trancoso", "Engineering", "Bachelor's")
            self.assertEqual(student.get_karma(), 0)

        with self.subTest("No reviews"):
            student = Student("Kwame Trancoso", "Engineering", "Bachelor's")
            mockReview = Review(1, 1, 4, "good")
            mockReview.vote(1, "up")
            student.reviews.append(mockReview)
            self.assertEqual(student.get_karma(), 1)

        with self.subTest("One negative review"):
            student = Student("Kwame Trancoso", "Engineering", "Bachelor's")
            mockReview1 = Review(1, 1, 1, "good")
            mockReview1.vote(1, "down")
            student.reviews.append(mockReview1)
            self.assertEqual(student.get_karma(), -1)


# Unit tests for Review model
class ReviewUnitTests(unittest.TestCase):
    def test_new_review(self):
        review = Review(1, 1, 4, "good")
        assert review.student_id == 1 and review.user_id == 1 and review.rating = 1 and review.comment == "good"

    def test_review_to_json(self):
        review = Review(1, 1, 4, "good")
        review_json = review.to_json()
        self.assertDictEqual(
            review_json,
            {
                "id": None,
                "user_id": 1,
                "student_id": 1,
                "comment": "good",
                "karma": 0,
                "num_upvotes": 0,
                "num_downvotes": 0
            },
        )

    def test_review_vote(self):
        with self.subTest("Upvote"):
            review = Review(1, 1, 4, "good")
            review.vote(1, "up")
            self.assertEqual(review.votes["num_upvotes"], 1)

        with self.subTest("Downvote"):
            review = Review(1, 1, "good")
            review.vote(1, "down")
            self.assertEqual(review.votes["num_downvotes"], 1)

    def test_review_get_num_upvotes(self):
        with self.subTest("No votes"):
            review = Review(1, 1, 4, "good")
            self.assertEqual(review.get_num_upvotes(), 0)

        with self.subTest("One upvote"):
            review = Review(1, 1, "good")
            review.vote(1, "up")
            self.assertEqual(review.get_num_upvotes(), 1)

        with self.subTest("One downvote"):
            review = Review(1, 1, "good")
            review.vote(1, "down")
            self.assertEqual(review.get_num_upvotes(), 0)

    def test_review_get_num_downvotes(self):
        with self.subTest("No votes"):
            review = Review(1, 1, 4, "good")
            self.assertEqual(review.get_num_downvotes(), 0)

        with self.subTest("One upvote"):
            review = Review(1, 1, 4, "good")
            review.vote(1, "up")
            self.assertEqual(review.get_num_downvotes(), 0)

        with self.subTest("One downvote"):
            review = Review(1, 1, 4, "good")
            review.vote(1, "down")
            self.assertEqual(review.get_num_downvotes(), 1)

    def test_review_get_karma(self):
        with self.subTest("No votes"):
            review = Review(1, 1, 4, "good")
            self.assertEqual(review.get_karma(), 0)

        with self.subTest("One upvote"):
            review = Review(1, 1, 4, "good")
            review.vote(1, "up")
            self.assertEqual(review.get_karma(), 1)

        with self.subTest("One downvote"):
            review = Review(1, 1, 4, "good")
            review.vote(1, "down")
            self.assertEqual(review.get_karma(), -1)

    def test_review_get_all_votes(self):
        with self.subTest("No votes"):
            review = Review(1, 1, 4, "good")
            self.assertEqual(
                review.get_all_votes(), {"num_upvotes": 0, "num_downvotes": 0}
            )

        with self.subTest("One upvote"):
            review = Review(1, 1, 4, "good")
            review.vote(1, "up")
            self.assertEqual(
                review.get_all_votes(), {1: "up", "num_upvotes": 1, "num_downvotes": 0}
            )

        with self.subTest("One downvote"):
            review = Review(1, 1, 4, "good")
            review.vote(1, "down")
            self.assertEqual(
                review.get_all_votes(),
                {1: "down", "num_upvotes": 0, "num_downvotes": 1},
            )

        with self.subTest("One upvote and one downvote"):
            review = Review(1, 1, 4, "good")
            review.vote(1, "up")
            review.vote(2, "down")
            self.assertEqual(
                review.get_all_votes(),
                {1: "up", 2: "down", "num_upvotes": 1, "num_downvotes": 1},
            )

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = create_user("bob", "bobpass")
    assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "bobpass")
        assert user.username == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"
