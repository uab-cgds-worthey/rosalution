""" Collection of FastAPI routes used for development and debugging the application """

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from ..config import Settings, get_settings
from ..dependencies import database
from ..security.oauth2 import HTTPBasicClientCredentials
from ..security.security import ( authenticate_password, create_access_token )

router = APIRouter(
    prefix="/dev",
    tags=["development"],
    dependencies=[Depends(database)],
)

token_scheme = HTTPBasicClientCredentials(auto_error=False, scheme_name="oAuth2ClientCredentials")

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
