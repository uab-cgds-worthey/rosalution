""" Collection of FastAPI routes used for development and debugging the application """

import asyncio
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.security import OAuth2PasswordRequestForm

from ..config import Settings, get_settings
from ..dependencies import DatabaseDepends, get_db
from ..security.oauth2 import HTTPBasicClientCredentials
from ..security.security import (authenticate_password, create_access_token)

router = APIRouter(prefix="/dev", tags=["development"])

token_scheme = HTTPBasicClientCredentials(auto_error=False, scheme_name="oAuth2ClientCredentials")


@router.post("/loginDev")
async def login_local_developer(
    response: Response,
    repositories: Annotated[dict, Depends(get_db)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    settings: Annotated[Settings, Depends(get_settings)],
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = await repositories["user"].find_by_username(form_data.username)
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

# async def start_database_session(database_client):
#     async with database_client.start_session() as session:
#         async with session.bind():   
#             await session.start_transaction()
#             try: 
#                 for x in range(60):
#                     yield f"event: heartbeat\ndata: {x}\n\n"
            
#                 await asyncio.sleep(1)
#             except asyncio.CancelledError as e:
#                 print("ITS CANCELD YO")
#                 print(e)
#             finally:
#                 await session.abort_transaction()

# @router.post("/dbTransaction")
# async def local_db_transaction_start(request: Request):
#     """Return the database instance stored in the application state."""
#     """A mocked database client which overrides the database depedency injected"""

#     # def mock_get_db() -> dict:
#     #     return async_db_client()

#     # app.dependency_overrides[get_db] = mock_get_db
#     return StreamingResponse(coordinates_generator(request.app.state.database.database_client), media_type="text/event-stream")

