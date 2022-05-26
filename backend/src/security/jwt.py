""" Handles creating the JWT token for the frontend """

from typing import Optional
from datetime import datetime, timedelta
from jose import jwt

from .. import constants

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """ Takes in information and uses JWT to create and return a proper access token """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, constants.SECRET_KEY, algorithm=constants.ALGORITHM)
    return encoded_jwt
