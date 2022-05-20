from pydantic import ValidationError
from jose import jwt, JWTError

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

from . import config
from .dependencies import database

from .core.user import User, UserInDB
from .core.token import TokenData

## Auth Utils

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/divergen/api/auth/token",
    scopes={
        "read": "View the pages on diverGen.",
        "write": "Add/Remove information from diverGen analyses.",
        "modify": "Add/Remove analyses themselves."
    }
)

def get_user(user_collection, username: str):
    user_dict = user_collection.find_by_name(username)
    return UserInDB(**user_dict)

async def get_authorization(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    if security_scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'        
    else:
        authenticate_value = f"Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Autenticate": authenticate_value}
    )
    
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])        
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return True

async def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    if security_scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'        
    else:
        authenticate_value = f"Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Autenticate": authenticate_value}
    )
    
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])        
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user_collection = database.collections['user']
    user = get_user(user_collection, username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user

async def get_current_active_user(current_user: User = Security(get_current_user, scopes=["read"])):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive User")
    return current_user
