"""
Manages the user collection of the users registered to rosalution
"""


class UserCollection:
    """Collection for users"""

    def __init__(self, users_collection):
        """Initializes with the 'PyMongo' Collection object for the users collection"""
        self.collection = users_collection

    def all(self):
        """Returns all users"""
        return self.collection.find()

    def find_by_username(self, username: str):
        """Returns user by searching for a user's name"""
        user = self.collection.find_one({"username": username})

        if user is None:
            return None

        user.pop("_id", None)
        return user
