"""
Manages the user collection of the users registered to diverGen
"""

from src.core.security import get_password_hash, verify_password

from ..utils import read_fixture

class UserCollection():
    """ Collection for user09ing users """

    def all(self):
        """ Returns all users in the system """
        return read_fixture("users.json")

    def find_by_name(self, name: str):
        """ Returns user by searching for user's name """
        users = read_fixture("users.json")
        for user in users:
            if user == name:
                return users[user]
        
        return None
    
    def authenticate_user(self, username: str, password: str):
        user = self.find_by_name(username)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user