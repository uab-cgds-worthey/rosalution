""" FastAPI Authentication router file that handles the auth lifecycle of the application """
from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Security, Response
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from starlette.requests import Request

from cas import CASClient
from src import config

from ..core.user import User, VerifyUser
from ..security.jwt import create_access_token
from ..security.security import get_current_user

from ..dependencies import database

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    dependencies=[Depends(database)],
)

# URLs for interacting with UAB CAS Padlock system for BlazerID
cas_client = CASClient(
    version=3,
    service_url='http://dev.cgds.uab.edu/divergen/api/auth/login?nexturl=%2Fdivergen',
    server_url='https://padlockdev.idm.uab.edu/cas/'
)

## CAS Login ##

# pylint: disable=no-member
# This is done because pylint doesn't appear to be recognizing python-cas's functions saying they have no member
@router.get('/login')
async def login(request: Request, nexturl: Optional[str] = None, ticket: Optional[str] = None):
    """ diverGen Login Method """
    if request.session.get("username", None):
        # We're already logged in, don't need to do the login process
        return {'url': 'http://dev.cgds.uab.edu/divergen/'}

    if not ticket:
        # No ticket, the request comes from end user, send to CAS login
        cas_login_url = cas_client.get_login_url()
        return {'url': cas_login_url}

    user, attributes, pgtiou = cas_client.verify_ticket(ticket)

    if not user:
        # Failed ticket verification, this should be an error page of some kind maybe?
        return RedirectResponse('http://dev.cgds.uab.edu/divergen/auth/login')

    # Login was successful, redirect to the 'nexturl' query parameter
    request.session['username'] = user
    request.session['attributes'] = attributes
    request.session['pgtiou'] = pgtiou
    base_url = 'http://dev.cgds.uab.edu'
    return RedirectResponse(base_url + nexturl)

@router.get('/get_user')
def get_user(request: Request):
    """ Returns active user in session """
    if 'username' in request.session:
        print(request.session)
        return {'username': request.session['username']}

    return {'username': ''}

@router.get('/logoutCas')
def logout(request: Request):
    """ Test Logout Method """
    redirect_url = request.url_for('login')
    cas_logout_url = cas_client.get_logout_url(redirect_url)
    request.session.pop("username", None)
    request.session.pop("attributes", None)
    request.session.pop("pgtiou", None)

    return {'url': cas_logout_url}

## OAuth2 Login ##

@router.post('/token')
def login_oauth(
        request: Request,
        response: Response,
        form_data: OAuth2PasswordRequestForm = Depends(),
        collections=Depends(database)
    ):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    collections['user'].authenticate_user(form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires
    )
    content = {"access_token": access_token, "token_type": "bearer"}
    response = JSONResponse(content=content)
    response.set_cookie(key='DIVERGEN_TOKEN', value=access_token)
    request.session['username'] = form_data.username
    return response

@router.get("/verify", response_model=User)
def issue_token(
        request: Request,
        collections=Depends(database),
        username: VerifyUser = Security(get_current_user, scopes=['read']),

    ):
    """ This function issues the authentication token for the frontend to make requests """
    if 'username' in request.session:
        print(request.session['username'])
    user_collection = collections['user']
    user = user_collection.find_by_name(username)
    current_user = User(**user)
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive User")

    return current_user

@router.get('/logout')
def logout_oauth(request: Request):
    """ Returns an empty access token """
    content = {'access_token': ''}
    response = JSONResponse(content=content)
    response.delete_cookie(key='DIVERGEN_TOKEN')
    if 'username' in request.session:
        request.session.pop('username', None)
    return response
