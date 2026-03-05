"""
This test module goes over the security.py file and tests what is
required for a user to successfully authenticate with the system
"""

from unittest.mock import Mock

import pytest

import jwt

from fastapi import HTTPException, Response
from fastapi.security import SecurityScopes
from src.config import Settings
from src.security.security import (
    authenticate_password, get_authorization, get_current_user, create_access_token, generate_client_secret,
    get_password_hash, get_project_authorization
)


def test_create_access_token(settings: Settings):
    """ This tests a successfully created access token """

    payload_to_encode = {'sub': 'johndoe', 'scopes': ['read']}

    actual_encoded_jwt = create_access_token(
        payload_to_encode,
        settings.oauth2_access_token_expire_minutes,
        settings.rosalution_key,
        settings.oauth2_algorithm,
    )

    assert actual_encoded_jwt is not None


def test_password_hash():
    """ Testing that the password given isn't what is returned """
    password = "fake-password"
    password_hash = get_password_hash(password)

    assert password != password_hash


def test_authorization_successful(settings):
    """Shows a completely successful authentication process and what is required"""
    security_scopes = SecurityScopes()
    security_scopes.scope_str = "read"
    security_scopes.scope_str = "read"
    payload = {"sub": "johndoe", "scopes": ["read"]}
    jwt.decode = Mock(return_value=payload)

    authorization = get_authorization(security_scopes, settings=settings)

    assert authorization is True


def test_authorization_unsuccessful_no_user(settings):
    """Fails to authenticate user in the system due to there not being a valid user decoded from the token"""
    security_scopes = SecurityScopes()
    payload = {"sub": None}

    jwt.decode = Mock(return_value=payload)
    with pytest.raises(HTTPException) as authorization_error:
        get_authorization(security_scopes, settings=settings)
        assert authorization_error.status_code == 401


def test_authorization_unsuccessful_not_in_scope(settings):
    """Our user exists, but their scope is Read and they're calling a Write scoped endpoint"""
    security_scopes = SecurityScopes()
    security_scopes.scopes = ["write"]
    security_scopes.scope_str = "write"
    payload = {"sub": "johndoe", "scopes": ["read"]}

    jwt.decode = Mock(return_value=payload)

    with pytest.raises(HTTPException) as authorization_error:
        get_authorization(security_scopes, settings=settings)
        assert authorization_error.status_code == 401


def test_current_user_existing_user(settings):
    """Successfully extracts the client_id from the auth token for use within the application"""
    payload = {
        "sub": "fake-client-id",
    }
    jwt.decode = Mock(return_value=payload)

    response = Response("fake response", media_type="text/plain")

    client_id = get_current_user(response, settings=settings)
    assert client_id == "fake-client-id"


def test_current_non_existing_user(settings):
    """ Handles when no user is encoded in the access token, providing an unauthorized """
    payload = {"sub": None}

    jwt.decode = Mock(return_value=payload)

    response = Response("fake response", media_type="text/plain")

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(response=response, settings=settings)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Could not validate credentials"


def test_authenticate_successful(user_john_doe):
    """ Successfully authenticates user password """
    user = authenticate_password(user_john_doe, "secret")

    assert user["full_name"] == "John Doe"
    assert user["email"] == "johndoe@example.com"


def test_authenticate_unsuccessful_no_user():
    """ Fails to authenticate given no user object passed in """
    authenticate_result = authenticate_password(None, "secret1")

    assert authenticate_result is None


def test_authenticate_unsuccessful_password(user_john_doe):
    """ Handles the incorrect password for a user """
    authenticate_result = authenticate_password(user_john_doe, "secret1")

    assert authenticate_result is None


def test_generate_client_secret():
    """ Tests to see if the client secret contains the correct length of characters """
    client_secret = generate_client_secret()

    assert len(client_secret) == 32


def test_project_authorization_successful(
    user_collection, analysis_collection, cpam0002_analysis_json, client_id_from_get_current_user
):
    """Shows a completely successful authentication process and what is required"""

    analysis_collection.project_id_by_name = Mock(return_value=str(cpam0002_analysis_json["project_id"]))

    database = {'user': user_collection, 'analysis': analysis_collection}

    analysis_name = "CPAM0002"
    authorization = get_project_authorization(
        analysis_name, repositories=database, client_id=client_id_from_get_current_user
    )

    assert authorization is True


@pytest.fixture(name="client_id_from_get_current_user")
def fixture_client_id_from_get_current_user(response_with_fake_client_id_pyaload, settings):
    """Fixture for retrieving the client_id from the response fixture according to the settings fixture"""
    client_id = get_current_user(response_with_fake_client_id_pyaload, settings=settings)
    return client_id


@pytest.fixture(name="response_with_fake_client_id_pyaload")
def fixture_reponse_with_fake_client_payload():
    """Fixture for emulating a Reqeuest Response that includes a payload for the javascript web token to decode"""
    payload = {
        "sub": "fake-client-id",
    }
    jwt.decode = Mock(return_value=payload)

    return Response("fake response", media_type="text/plain")


@pytest.fixture(name="user_john_doe")
def fixture_user_john_doe(users_json):
    """Fixture for the user John Doe from the users collection JSON"""
    return next((user for user in users_json if user['full_name'] == "John Doe"), None)
