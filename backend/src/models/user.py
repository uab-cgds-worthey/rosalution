""" Represents a user that is stored in our database """
# pylint: disable=too-few-public-methods

from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    """Basic information need for a registered user"""

    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    scope: Optional[str] = None


class VerifyUser(User):
    """Hashed password was omitted from the base object as it's not always needed"""

    hashed_password: str
