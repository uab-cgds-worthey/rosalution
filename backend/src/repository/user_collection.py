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

    def find_by_client_id(self, client_id: str):
        """ Returns user by searching for a user's client id """
        user = self.collection.find_one({"client_id": client_id})

        if user is None:
            return None

        user.pop("_id", None)
        return user

    def update_client_secret(self, client_id: str, client_secret: str):
        """  """
        user = self.collection.find_one_and_update({'client_id': client_id},{'$set': {'client_secret': client_secret}})

        if user is None:
            return None

        user.pop("_id", None)

        print(user)

        return user