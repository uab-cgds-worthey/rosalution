""" Provides necessary functions to handle passwords and determining whether users are a verified user  """

import secrets
import string

from datetime import datetime, timedelta, UTC
from typing import Optional

import jwt

from pydantic import ValidationError
from jwt.exceptions import InvalidTokenError

from fastapi import Depends, HTTPException, Response, status
from fastapi.security import SecurityScopes

import bcrypt

from ..dependencies import oauth2_scheme

from ..config import Settings, get_settings

SECURITY_SCOPES = {
    "pre-clinical-intake": "Pre-Clinical Intake",
    "bioinformatics-section-user": "Bioinformatics Section User",
    "researcher": "Researcher",
    "developer": "Developer",
}


def create_access_token(
    data: dict,
    access_token_expiration_minutes,
    secret_token,
    algorithm,
    expires_delta: Optional[timedelta] = None,
):
    """Takes in information and uses JWT to create and return a proper access token"""
    access_token_expires = timedelta(minutes=access_token_expiration_minutes)

    if expires_delta is not None:
        access_token_expires = expires_delta

    to_encode = data.copy()
    if access_token_expires:
        expire = datetime.now(UTC) + access_token_expires
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_token, algorithm)
    return encoded_jwt


def get_password_hash(password):
    """Takes the plain password and makes a hash from it using CryptContext"""
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password


def verify_password(plain_password, hashed_password):
    """This will use the CryptContext to hash the plain password and check against the stored pass hash to verify"""
    password_byte_encoded = plain_password.encode('utf-8')
    hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password=password_byte_encoded, hashed_password=hashed_password)


def authenticate_password(user: Optional[dict], password: str):
    """Takes a username string and a password string, finds the user, verfies the password and returns a user"""
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user


def generate_client_secret():
    """ This generates a client secret for a user upon request """
    alphabet = string.ascii_letters + string.digits
    client_secret = ''.join(secrets.choice(alphabet) for i in range(32))
    return client_secret


def get_current_user(
    response: Response, token: str = Depends(oauth2_scheme), settings: Settings = Depends(get_settings)
):
    """Extracts the client_id from the token, this is useful to ensure the user is who they say they are"""
    authenticate_value = "Bearer"

    try:
        payload = jwt.decode(token, settings.rosalution_key, algorithms=[settings.oauth2_algorithm])
        client_id: str = payload.get("sub")
        if client_id is None:
            response.delete_cookie(key="rosalution_TOKEN")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Autenticate": authenticate_value, "set-cookie": response.headers["set-cookie"]},
            )
    except InvalidTokenError as jwt_error:
        response.delete_cookie(key="rosalution_TOKEN")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not a valid token: " + str(jwt_error),
            headers={"WWW-Authenticate": authenticate_value, "set-cookie": response.headers["set-cookie"]},
        ) from jwt_error

    return client_id


def get_authorization(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
    settings: Settings = Depends(get_settings),
):
    """
    This function does a general authorization check to see if the user is authorized and within scope to use the
    endpoint that is requested.

    This will be used when scopes are implemented with the users. For now, authorization will use "get_current_user.
    """
    if security_scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Autenticate": authenticate_value},
    )

    try:
        payload = jwt.decode(token, settings.rosalution_key, algorithms=[settings.oauth2_algorithm])
        client_id: str = payload.get("sub")
        if client_id is None:
            raise credentials_exception
        user_scopes = payload.get("scopes", str)
    except (InvalidTokenError, ValidationError) as validation_exception:
        raise validation_exception
    # for scope in security_scopes.scopes:
    if "write" in security_scopes.scopes and "write" not in user_scopes:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not enough permissions",
            headers={"WWW-Authenticate": authenticate_value},
        )

    return True
