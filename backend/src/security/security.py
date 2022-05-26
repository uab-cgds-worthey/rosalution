""" Provides necessary functions to handle passwords and determining whether users are a verified user  """

from pydantic import ValidationError
from jose import jwt, JWTError

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

from passlib.context import CryptContext

from .. import constants
from ..core.token import TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=constants.TOKEN_URL,
    scopes=constants.SECURITY_SCOPES
)

def verify_password(plain_password, hashed_password):
    """ This will use the CryptContext to hash the plain password and check against the stored pass hash to verify """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """ This function takes the plain password and makes a hash from it using CryptContext """
    return pwd_context.hash(password)

def get_authorization(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    """
    This function does a general authorization check to see if the user is authorized and within scope to use the
    endpoint that is requested.
    """
    if security_scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Autenticate": authenticate_value}
    )

    try:
        payload = jwt.decode(token, constants.SECRET_KEY, algorithms=[constants.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError) as validation_exception:
        raise validation_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return True


## Verify User
## We get the user from the token provided by the user to ensure it's the correct user

def get_current_user(token: str = Depends(oauth2_scheme)):
    """ Extracts the username from the token, this is useful to ensure the user is who they say they are """
    authenticate_value = "Bearer"

    try:
        payload = jwt.decode(token, constants.SECRET_KEY, algorithms=[constants.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Autenticate": authenticate_value}
                )
    except JWTError as jwt_error:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail = "Not a valid token: " + str(jwt_error),
                headers={"WWW-Authenticate": authenticate_value}
            ) from jwt_error

    return username
