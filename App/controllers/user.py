from App.models import User
from App.database import db

# Creates a new user
def create_user(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit() 
    return newuser

# Gets the desired user given their username
def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

# Gets the desired user given their id
def get_user(id):
    return User.query.get(id)

# Gets all created users
def get_all_users():
    return User.query.all()

# Gets all created users in a JSON object
def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

# Updates a user given selected parameters
def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None
    
