import pytest

from unittest.mock import Mock

from jose import jwt

from fastapi import HTTPException
from fastapi.security import SecurityScopes
from src.security.security import get_authorization, get_current_user

def test_authorization_successful():
    security_scopes = SecurityScopes()
    security_scopes.scope_str = 'read'
    security_scopes.scope_str = 'read'
    payload = {
            'sub': 'johndoe', 
            'scopes': ['read']
        }
    jwt.decode = Mock(
        return_value=payload
    )

    authorization = get_authorization(security_scopes)

    assert authorization == True

def test_authorization_unsuccessful_no_user():
    security_scopes = SecurityScopes()
    payload = { 'sub': None }

    jwt.decode = Mock(
        return_value=payload
    )
    with pytest.raises(HTTPException) as authorization_error:
        get_authorization(security_scopes)
        assert authorization_error.status_code == 401

def test_authorization_unsuccessful_not_in_scope():
    """ Our user exists, but their scope is Read and they're calling a Write scoped endpoint """
    security_scopes = SecurityScopes()
    security_scopes.scopes = ['write']
    security_scopes.scope_str = 'write'
    payload = {
            'sub': 'johndoe', 
            'scopes': ['read']
        }

    jwt.decode = Mock(
        return_value=payload
    )

    with pytest.raises(HTTPException) as authorization_error:
        get_authorization(security_scopes)
        assert authorization_error.status_code == 401

def test_current_user_existing_user():
    payload = {
        'sub': 'johndoe',
    }
    jwt.decode = Mock(
        return_value=payload
    )

    username = get_current_user()
    assert username == 'johndoe'