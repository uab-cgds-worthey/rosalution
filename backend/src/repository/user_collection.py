"""
Manages the user collection of the users registered to rosalution
"""
from pymongo import ReturnDocument


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

    def find_by_client_id(self, client_id: str):
        """ Returns user by searching for a user's client id """
        user = self.collection.find_one({"client_id": client_id})

        if user is None:
            return None

        user.pop("_id", None)
        return user

    def update_client_secret(self, client_id: str, client_secret: str):
        """ Takes a generated client secret and saves it the user with the associated client id """
        user = self.collection.find_one_and_update({'client_id': client_id}, {'$set': {'client_secret': client_secret}},
                                                   return_document=ReturnDocument.AFTER)

        print(user)

        if user is None:
            return None

        user.pop("_id", None)

        return user
