""" Represents a user that is stored in our database """
# pylint: disable=too-few-public-methods

from typing import Annotated, List, Optional

from pydantic import BaseModel, BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]


class User(BaseModel):
    """Basic information need for a registered user"""

    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    scope: Optional[str] = None
    client_id: str


class AccessUserAPI(User):
    """ This extends the user class to include the user's credentials for API access """
    client_secret: Optional[str] = None


class VerifyUser(User):
    """Hashed password was omitted from the base object as it's not always needed"""

    hashed_password: str


class ProjectUser(User):
    """ This extends the use class to include project_id """
    project_ids: List[PyObjectId] = []

    def is_authorized(self, project_id: PyObjectId):
        """Returns true if user is authorized to access content by a project's ID"""

        return any(project_id == user_project_id for user_project_id in self.project_ids)
