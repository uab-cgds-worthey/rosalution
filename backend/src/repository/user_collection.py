"""
Manages the user collection of the users registered to rosalution
"""
from ..security.security import verify_password


class UserCollection:
    """Collection for user09ing users"""

    def __init__(self, users_collection):
        """Initializes with the 'PyMongo' Collection object for the users collection"""
        self.collection = users_collection

    def all(self):
        """Returns all annotation configurations"""
        return self.collection.find()

    def find_by_username(self, username: str):
        """Returns user by searching for user's name"""
        return self.collection.find_one({ "username": username })

    def authenticate_user(self, username: str, password: str):
        """Takes a username string and a password string, finds the user, verfies the password and returns a user"""
        user = self.find_by_username(username)
        if not user:
            return None
        if not verify_password(password, user["hashed_password"]):
            return False
        return user
