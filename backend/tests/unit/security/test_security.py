"""
This test module goes over the security.py file and tests what is
required for a user to successfully authenticate with the system
"""

from unittest.mock import Mock

import pytest

from jose import jwt

from fastapi import HTTPException
from fastapi.security import SecurityScopes
from src.security.security import get_authorization, get_current_user, create_access_token


def test_create_access_token():
    """ This tests a successfully created access token """

    payload = {'sub': 'johndoe', 'scopes': ['read']}

    actual_encoded_jwt = create_access_token(payload)

    assert actual_encoded_jwt is not None

def test_authorization_successful():
    """Shows a completely successful authentication process and what is required"""
    security_scopes = SecurityScopes()
    security_scopes.scope_str = "read"
    security_scopes.scope_str = "read"
    payload = {"sub": "johndoe", "scopes": ["read"]}
    jwt.decode = Mock(return_value=payload)

    authorization = get_authorization(security_scopes)

    assert authorization is True


def test_authorization_unsuccessful_no_user():
    """Fails to authenticate user in the system due to there not being a valid user decoded from the token"""
    security_scopes = SecurityScopes()
    payload = {"sub": None}

    jwt.decode = Mock(return_value=payload)
    with pytest.raises(HTTPException) as authorization_error:
        get_authorization(security_scopes)
        assert authorization_error.status_code == 401


def test_authorization_unsuccessful_not_in_scope():
    """Our user exists, but their scope is Read and they're calling a Write scoped endpoint"""
    security_scopes = SecurityScopes()
    security_scopes.scopes = ["write"]
    security_scopes.scope_str = "write"
    payload = {"sub": "johndoe", "scopes": ["read"]}

    jwt.decode = Mock(return_value=payload)

    with pytest.raises(HTTPException) as authorization_error:
        get_authorization(security_scopes)
        assert authorization_error.status_code == 401


def test_current_user_existing_user():
    """Successfully extracts the username from the auth token for use within the application"""
    payload = {
        "sub": "johndoe",
    }
    jwt.decode = Mock(return_value=payload)

    username = get_current_user()
    assert username == "johndoe"
