"""
Manages the user collection of the users registered to rosalution
"""
# pylint: disable=no-self-use
# This linting disable will be removed once database is added
from ..security.security import verify_password
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
        """ Takes a username string and a password string, finds the user, verfies the password and returns a user """
        user = self.find_by_name(username)
        if not user:
            return False
        if not verify_password(password, user['hashed_password']):
            return False
        return user
