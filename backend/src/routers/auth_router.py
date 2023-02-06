""" FastAPI Authentication router file that handles the auth lifecycle of the application """
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Security, Response, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

from starlette.requests import Request

from cas import CASClient

from ..config import Settings, get_settings
from ..dependencies import database
from ..models.user import User, VerifyUser, AccessUserAPI
from ..security.oauth2 import OAuth2ClientCredentialsRequestForm, HTTPClientCredentials, HTTPBasicClientCredentials
from ..security.security import (
    authenticate_password, create_access_token, get_authorization, get_current_user, generate_client_secret
)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    dependencies=[Depends(database)],
)

# URLs for interacting with UAB CAS Padlock system for BlazerID
cas_client = CASClient(
    version=3,
    service_url=get_settings().cas_api_service_url,
    server_url=get_settings().cas_server_url,
)

token_scheme = HTTPBasicClientCredentials(auto_error=False, scheme_name="oAuth2ClientCredentials")


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
@router.get("/login", include_in_schema=False)
async def login(
    response: Response,
    nexturl: Optional[str] = None,  # CAS Nexturl
    ticket: Optional[str] = None,
    repositories=Depends(database),
    settings: Settings = Depends(get_settings),
):
    """Rosalution Login Method"""
    if not ticket:
        # No ticket, the request comes from end user, send to CAS login
        cas_login_url = cas_client.get_login_url()
        return {"url": cas_login_url}

    # These are returned by UAB CAS login, but they are unused beyond the user value
    # pylint: disable=unused-variable
    cas_user, attributes, pgtiou = cas_client.verify_ticket(ticket)

    if not cas_user:
        print("Failed Padlock ticket user verification, redirect back to login page")
        # Failed ticket verification, this should be an error page of some kind maybe?

        redirect_frontend_route_response = settings.web_base_url + settings.auth_web_failure_redirect_route
        return RedirectResponse(redirect_frontend_route_response)

    # Login was successful, redirect to the 'nexturl' query parameter
    user = repositories["user"].find_by_username(cas_user)

    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized Rosalution user")

    data_to_encode = {
        "sub": user['client_id'],
        "scopes": [user['scope']],
    }
    access_token = create_access_token(
        data_to_encode, settings.oauth2_access_token_expire_minutes, settings.rosalution_key, settings.oauth2_algorithm
    )

    response = RedirectResponse(url=settings.web_base_url + nexturl)
    response.delete_cookie(key="rosalution_TOKEN")
    response.set_cookie(key="rosalution_TOKEN", value=access_token)

    return response


@router.post("/loginDev")
def login_local_developer(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    repositories=Depends(database),
    settings: Settings = Depends(get_settings),
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = repositories["user"].find_by_username(form_data.username)
    user_authenticated = authenticate_password(user, form_data.password)

    if not user_authenticated:
        raise HTTPException(status_code=401, detail="Unauthorized Rosalution user")

    data_to_encode = {
        "sub": user_authenticated['client_id'],
        "scopes": [user_authenticated['scope']],
    }
    access_token = create_access_token(
        data_to_encode, settings.oauth2_access_token_expire_minutes, settings.rosalution_key, settings.oauth2_algorithm
    )

    content = {"access_token": access_token, "token_type": "bearer"}
    response = JSONResponse(content=content)
    response.delete_cookie(key='rosalution_TOKEN')
    response.set_cookie(key="rosalution_TOKEN", value=access_token)

    return response


@router.post("/token")
def issue_oauth2_token(
    form_data: OAuth2ClientCredentialsRequestForm = Depends(),
    basic_credentials: Optional[HTTPClientCredentials] = Depends(token_scheme),
    repositories=Depends(database),
    settings: Settings = Depends(get_settings),
):
    """
    Issues a valid OAuth2 token upon recieving valid client_id and client_secret
    """
    if form_data.client_id and form_data.client_secret:
        client_id = form_data.client_id
        client_secret = form_data.client_secret
    elif basic_credentials:
        client_id = basic_credentials.client_id
        client_secret = basic_credentials.client_secret
    else:
        raise HTTPException(status_code=400, detail="Client credentials not provided")

    user = repositories["user"].find_by_client_id(client_id)

    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized Rosalution user")

    credentialed_user = AccessUserAPI(**user)

    if client_secret != credentialed_user.client_secret:
        raise HTTPException(status_code=401, detail="Unauthorized Rosalution user")

    data_to_encode = {
        "sub": user['client_id'],
        "scopes": [user['scope']],
    }
    access_token = create_access_token(
        data_to_encode, settings.oauth2_access_token_expire_minutes, settings.rosalution_key, settings.oauth2_algorithm
    )

    content = {"access_token": access_token, "token_type": "bearer"}

    return content


@router.get("/verify_token", response_model=User)
def verify_token(
    repositories=Depends(database),
    client_id: VerifyUser = Security(get_current_user),
):
    """This function issues the authentication token for the frontend to make requests"""
    user = repositories["user"].find_by_client_id(client_id)

    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    current_user = User(**user)

    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive User")

    return current_user


@router.get("/generate_secret", status_code=status.HTTP_201_CREATED)
def generate_secret(client_id: VerifyUser = Security(get_current_user), repositories=Depends(database)):
    """ Generates and saves a client secret to a user upon request """

    client_secret = generate_client_secret()
    user = repositories["user"].update_client_secret(client_id, client_secret)

    if not user:
        raise HTTPException(status_code=500, detail="Something went wrong. Unable to create client secret.")

    credentialed_user = AccessUserAPI(**user)

    return credentialed_user


@router.get('/get_user_credentials')
def fetch_user_api_creds(client_id: VerifyUser = Security(get_current_user), repositories=Depends(database)):
    """ This is a special endpoint that returns the user along with their credentials for API access """
    user = repositories['user'].find_by_client_id(client_id)

    if not user:
        raise HTTPException(status_code=500, detail="Something went wrong. Unable to create client secret.")

    credentialed_user = AccessUserAPI(**user)

    return credentialed_user


@router.get("/logout")
def logout_oauth(request: Request, response: Response, settings: Settings = Depends(get_settings)):
    """ Destroys the session and determines if the request was local or production and returns the proper url """

    content = {"access_token": ""}

    if settings.cas_login_enable:
        redirect_url = request.url_for("logout_callback")
        cas_logout_url = cas_client.get_logout_url(redirect_url)
        content = {"url": cas_logout_url}

    response = JSONResponse(content=content)
    response.delete_cookie(key="rosalution_TOKEN")

    return response


@router.get('/logout_callback', include_in_schema=False)
def logout_callback(settings: Settings = Depends(get_settings)):
    """
    The endpoint that gets called after the production logout function is called and redirects
    back to the login page
    """
    redirect_url = settings.web_base_url + settings.auth_web_failure_redirect_route
    return RedirectResponse(url=redirect_url)
