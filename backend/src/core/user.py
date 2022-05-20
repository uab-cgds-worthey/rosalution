import array
from typing import Optional

from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    scope: Optional[str] = None

class UserInDB(User):
    hashed_password: str