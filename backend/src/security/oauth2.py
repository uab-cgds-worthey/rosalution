from typing import Optional

from fastapi.exceptions import HTTPException
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import HTTPBasic
from fastapi.security.oauth2 import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi.param_functions import Form

from pydantic import BaseModel

class HTTPClientCredentials(BaseModel):
    client_id: str
    client_secret: str

class HTTPBasicClientCredentials(HTTPBasic):
    async def __call__(  # type:ignore
        self, request: Request
    ) -> Optional[HTTPClientCredentials]:
        basic = await super().__call__(request)
        if not basic:
            return None
        return HTTPClientCredentials(
            client_id=basic.username, client_secret=basic.password
        )

class OAuth2ClientCredentials(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = "oAuth2ClientCredentials",
        scopes: dict = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(
            clientCredentials={"tokenUrl": tokenUrl, "scopes": scopes}
        )
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
            else:
                return None
        return param

class OAuth2ClientCredentialsRequestForm:
    def __init__(
        self,
        grant_type: str = Form(None, regex="client_credentials"),
        scope: str = Form(""),
        client_id: Optional[str] = Form(None),
        client_secret: Optional[str] = Form(None),
    ):
        self.grant_type = grant_type
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret
