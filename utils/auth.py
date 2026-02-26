from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id):
        self.id = id

# simple demo user
users = {"admin": {"password": "1234"}}