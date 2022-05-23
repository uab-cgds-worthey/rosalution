""" FastAPI Authentication router file that handles the auth lifecycle of the application """
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordRequestForm

from ..core.user import User, UserInDB
from ..security.jwt import create_access_token
from ..security.security import get_current_user

from ..dependencies import database

from src import config

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    dependencies=[Depends(database)],
)

@router.post('/token')
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    print(form_data.scopes)
    user_collection = database.collections['user']
    user_collection.authenticate_user(user_collection, form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/verify", response_model=User)
def test_token(username: UserInDB = Security(get_current_user, scopes=['read'])):
    print(username)
    user = database.collections['user'].find_by_name(username)
    current_user = User(**user)
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive User")
    
    return current_user

## Disabling for now

# from cas import CASClient
# from typing import Optional
# from fastapi.responses import RedirectResponse
# from starlette.requests import Request

# URLs for interacting with UAB CAS Padlock system for BlazerID
# cas_client = CASClient(
#     version=3,
#     service_url='http://dev.cgds.uab.edu/divergen/api/auth/login?nexturl=%2Fdivergen',
#     server_url='https://padlockdev.idm.uab.edu/cas/'
# )

# pylint: disable=no-member
# This is done because pylint doesn't appear to be recognizing python-cas's functions saying they have no member
# @router.get('/login')
# async def login(request: Request, nexturl: Optional[str] = None, ticket: Optional[str] = None):
#     """ diverGen Login Method """
#     if request.session.get("username", None):
#         # We're already logged in, don't need to do the login process
#         return {'url': 'http://dev.cgds.uab.edu/divergen/'}

#     if not ticket:
#         # No ticket, the request comes from end user, send to CAS login
#         cas_login_url = cas_client.get_login_url()
#         return {'url': cas_login_url}

#     user, attributes, pgtiou = cas_client.verify_ticket(ticket)

#     if not user:
#         # Failed ticket verification, this should be an error page of some kind maybe?
#         return RedirectResponse('http://dev.cgds.uab.edu/divergen/auth/login')

#     # Login was successful, redirect to the 'nexturl' query parameter
#     request.session['username'] = user
#     request.session['attributes'] = attributes
#     request.session['pgtiou'] = pgtiou
#     base_url = 'http://dev.cgds.uab.edu'
#     return RedirectResponse(base_url + nexturl)

# @router.get('/get_user')
# def get_user(request: Request):
#     """ Returns active user in session """
#     if 'username' in request.session:
#         return {'username': request.session['username']}

#     return {'username': ''}

# @router.get('/logout')
# def logout(request: Request):
#     """ Test Logout Method """
#     redirect_url = request.url_for('login')
#     cas_logout_url = cas_client.get_logout_url(redirect_url)
#     request.session.pop("username", None)
#     request.session.pop("attributes", None)
#     request.session.pop("pgtiou", None)

#     return {'url': cas_logout_url}
