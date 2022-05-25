from src.security import get_password_hash

def test_authorization():
    get_password_hash("abc", "abc")
    assert 1 == 1