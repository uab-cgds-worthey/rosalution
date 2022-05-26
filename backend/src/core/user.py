""" Represents a user that is stored in our database """
# pylint: disable=too-few-public-methods

from typing import Optional

from pydantic import BaseModel

class User(BaseModel):
    """ The most basic information that is needed by the application pretatining to a registered user """
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    scope: Optional[str] = None

class UserInDB(User):
    """ Hashed password was omitted from the base object as it's not always needed """
    hashed_password: str
