""" FastAPI Authentication router file that handles the auth lifecycle of the application """
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Security, Response
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from starlette.requests import Request

from cas import CASClient

from ..models.user import User, VerifyUser
from ..security.security import get_authorization, get_current_user, create_access_token

from ..dependencies import database

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    dependencies=[Depends(database)],
)

# URLs for interacting with UAB CAS Padlock system for BlazerID
cas_client = CASClient(
    version=3,
    service_url="http://dev.cgds.uab.edu/rosalution/api/auth/login?nexturl=%2Frosalution",
    server_url="https://padlockdev.idm.uab.edu/cas/",
)

## Test Route ##
@router.get("/dev_only_test")
def test(authorized=Security(get_authorization, scopes=["developer"])):
    """ Only developers can hit this endpoint """
    print(authorized)
    return {
        "Ka": ["Boom", "Blammo", "Pow"],
    }

# pylint: disable=no-member
# This is done because pylint doesn't appear to be recognizing python-cas's functions saying they have no member
@router.get("/login")
async def login(
    request: Request,
    response: Response,
    nexturl: Optional[str] = None,
    ticket: Optional[str] = None,
    repositories=Depends(database)
):
    """Rosalution Login Method"""
    request.session.pop("attributes", None)
    request.session.pop("pgtiou", None)
    request.session.pop("username", None)
    request.session.pop("local", None)

    if not ticket:
        # No ticket, the request comes from end user, send to CAS login
        cas_login_url = cas_client.get_login_url()
        return {"url": cas_login_url}

    user, attributes, pgtiou = cas_client.verify_ticket(ticket)

    if not user:
        # Failed ticket verification, this should be an error page of some kind maybe?
        return RedirectResponse("http://dev.cgds.uab.edu/rosalution/auth/login")

    # Login was successful, redirect to the 'nexturl' query parameter
    authenticate_user = repositories["user"].authenticate_user(user, 'secret')

    if not authenticate_user:
        raise HTTPException(status_code=401, detail="Unauthorized Rosalution user")

    access_token = create_access_token(
        data={
            "sub": authenticate_user['username'],
            "scopes": [authenticate_user['scope']]
        }
    )

    request.session["username"] = authenticate_user['username']
    request.session["attributes"] = attributes
    request.session["pgtiou"] = pgtiou
    request.session["local"] = False

    base_url = "http://dev.cgds.uab.edu"

    response = RedirectResponse(url=base_url+nexturl)
    response.set_cookie(key="rosalution_TOKEN", value=access_token)

    return response

# This needs to be /token for the api/docs to work in issuing and recognizing a bearer
@router.post("/token", response_model=User)
def login_local_developer(
    request: Request,
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    repositories=Depends(database),
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    authenticate_user = repositories["user"].authenticate_user(
        form_data.username, form_data.password)

    if not authenticate_user:
        raise HTTPException(status_code=401, detail="Unauthorized Rosalution user")

    access_token = create_access_token(
        data={
            "sub": authenticate_user['username'],
            "scopes": [authenticate_user['scope']]
        }
    )

    content = {"access_token": access_token, "token_type": "bearer"}
    response = JSONResponse(content=content)
    response.set_cookie(key="rosalution_TOKEN", value=access_token)
    request.session["username"] = authenticate_user['username']
    request.session["local"] = True

    return response

@router.get("/verify_token", response_model=User)
def verify_token(
    repositories=Depends(database),
    username: VerifyUser = Security(get_current_user),
):
    """This function issues the authentication token for the frontend to make requests"""
    user = repositories["user"].find_by_username(username)
    current_user = User(**user)
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive User")

    return current_user

@router.get("/logout")
def logout_oauth(request: Request, response: Response):
    """ Destroys the session and determines if the request was local or production and returns the proper url """

    content = None

    if request.session['local'] is False:
        redirect_url = request.url_for("logout_callback")
        cas_logout_url = cas_client.get_logout_url(redirect_url)
        content = {"url": cas_logout_url}

    if request.session['local'] is True:
        content = {"access_token": ""}

    request.session.pop("attributes", None)
    request.session.pop("pgtiou", None)
    request.session.pop("username", None)
    request.session.pop("local", None)

    response = JSONResponse(content=content)
    response.delete_cookie(key="rosalution_TOKEN")

    return response

@router.get('/logout_callback')
def logout_callback():
    """
    The endpoint that gets called after the production logout function is called and redirects
    back to the login page
    """
    return RedirectResponse(url='http://dev.cgds.uab.edu/rosalution/login')
