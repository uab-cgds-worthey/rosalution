from typing import Optional

import jwt

from datetime import datetime, timedelta

ALGORITHM = "HS256"
SECRET_KEY = "ed6b87fcaf3be62fd13bcdcb2d5de7acccc30d35b1b01f8f6b8fe273c34df0bd"

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt