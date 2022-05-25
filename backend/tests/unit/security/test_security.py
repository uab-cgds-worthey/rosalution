from src.security.security import get_authorization

def test_authorization():
    security_scopes = ['write']
    get_authorization(security_scopes)
    assert 1 == 1

