"""Authentication Routes Intergration test"""
import json
from base64 import b64encode
from cas import CASClient
from itsdangerous import TimestampSigner

# Helper functions

def create_session_cookie(data) -> str:
    """ Function that creates a fake session token cookie to mimic Starlette session middleware """
    signer = TimestampSigner(str('!secret'))

    return signer.sign(b64encode(json.dumps(data).encode('utf-8')),).decode('utf-8')

# Authentication Tests #

def test_login_no_session(client):
    """ Testing the login endpoint when there is no login session already """
    response = client.get('/auth/login')
    assert response.json()['url'] == 'https://padlockdev.idm.uab.edu/cas/login?service=http%3A' + \
                                     '%2F%2Fdev.cgds.uab.edu%2Frosalution%2Fapi%2Fauth%2Flogin%3Fnexturl%3D%252Frosalution'


def test_login_existing_session(client):
    """ Testing the login endpoint when there is an existing login session """
    response = client.get(
        '/auth/login', cookies={'session': create_session_cookie({'username': 'UABProvider'})})
    assert response.json()['url'] == 'http://dev.cgds.uab.edu/rosalution/'


def test_login_successful(client, monkeypatch):
    """ Testing the login endpoint when there's a successful login and redirect """
    cas_client = CASClient(
        version=3,
        service_url='http://fake.url/auth/login',
        server_url='https://fake.url/cas/'
    )

    def mock_verify_return():
        return '<cas:serviceresponse xmlns:cas="http://www.yale.edy/tp/cas"> \
                    <cas:authenticationsuccess> \
                        <cas:user>UABProvider</cas:user> \
                    </cas:authenticationsuccess> \
                </cas:serviceresponse>"'

    monkeypatch.setattr(cas_client, "verify_ticket", mock_verify_return)

    response = client.get('/auth/login?nexturl=%2Frosalution&ticket=FakeTicketString')

    assert response.url == 'http://dev.cgds.uab.edu/rosalution/auth/login'


def test_get_user_not_logged_in(client):
    """ Testing the get_user endpoint when there is no user saved in the session """
    response = client.get('/auth/get_user')
    assert response.json()['username'] == ''


def test_get_user_logged_in(client):
    """ Testing if the logged in user returns the proper username """
    response = client.get(
        '/auth/get_user', cookies={'session': create_session_cookie({'username': 'UABProvider'})})
    assert response.json()['username'] == 'UABProvider'


def test_logout(client):
    """ Testing the log out functionality """
    response = client.get('/auth/logoutCas')
    assert response.json()['url'] == 'https://padlockdev.idm.uab.edu/cas/logout?' \
                                     'service=http%3A%2F%2Ftestserver%2Frosalution%2Fapi%2Fauth%2Flogin'
