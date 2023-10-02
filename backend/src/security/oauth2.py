"""
Function overrides necessary for the Swagger documents to use client id and client secret
instead of a username and password flow.
"""
# Disabling linting rules as it is FastAPI code just being overridden.
# pylint: disable=too-few-public-methods
from typing import Optional

from fastapi.exceptions import HTTPException
from fastapi.param_functions import Form
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import HTTPBasic
from fastapi.security.oauth2 import OAuth2
from fastapi.security.utils import get_authorization_scheme_param

from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

from pydantic import BaseModel


class HTTPClientCredentials(BaseModel):
    """ Defines credentials to use client_id and client_secret over username and password """
    client_id: str
    client_secret: str


class HTTPBasicClientCredentials(HTTPBasic):
    """ Handles network request for transmitting credentials via Swagger authorize """

    async def __call__(  # type:ignore
        self, request: Request
    ) -> Optional[HTTPClientCredentials]:
        basic = await super().__call__(request)
        if not basic:
            return None
        return HTTPClientCredentials(client_id=basic.username, client_secret=basic.password)


class OAuth2ClientCredentials(OAuth2):
    """ Updates the flow from username and password to client credentials for Swagger """

    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = "oAuth2ClientCredentials",
        scopes: dict = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(clientCredentials={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        return param


class OAuth2ClientCredentialsRequestForm:
    """ Changes the input form for the Swagger authorize to use client credentials """

    def __init__(
        self,
        grant_type: str = Form(None, pattern="client_credentials"),
        scope: str = Form(""),
        client_id: Optional[str] = Form(None),
        client_secret: Optional[str] = Form(None),
    ):
        self.grant_type = grant_type
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret
