"""Authentication Routes Intergration test"""
import json
from base64 import b64encode
from itsdangerous import TimestampSigner

from src.routers.auth_router import cas_client

# Helper functions

def create_session_cookie(data) -> str:
    """Function that creates a fake session token cookie to mimic Starlette session middleware"""
    signer = TimestampSigner(str("!secret"))

    return signer.sign(
        b64encode(json.dumps(data).encode("utf-8")),
    ).decode("utf-8")

# # Authentication Tests #

def test_login_no_session(client):
    """Testing the login endpoint when there is no login session already"""
    response = client.get("/auth/login")
    assert (
        response.json()["url"]
        == "https://padlockdev.idm.uab.edu/cas/login?service=http%3A"
        + "%2F%2Fdev.cgds.uab.edu%2Frosalution%2Fapi%2Fauth%2Flogin%3Fnexturl%3D%252Frosalution"
    )

def test_login_successful(client, mock_repositories, monkeypatch):
    """Testing the login endpoint when there's a successful login and redirect"""
    # This unused parameter is required for the monkeypatch to successfully use the mock verify function,
    # if no empty paramter is provided then the tests will crash.
    def mock_verify_return(paramater): #pylint: disable=unused-argument
        return (
            '<cas:serviceresponse xmlns:cas="http://www.yale.edy/tp/cas">                    ',
            " <cas:authenticationsuccess>                         <cas:user>UABProvider</cas:user>                    ",
            ' </cas:authenticationsuccess>                 </cas:serviceresponse>"'
        )

    monkeypatch.setattr(cas_client, "verify_ticket", mock_verify_return)

    mock_repositories['user'].collection.find_one.return_value = {
        "username": "UABProvider",
        "scope": ['fakescope'],
        "hashed_password": "$2b$12$xmKVVuGh6e0wP1fKellxMuOZ8HwVoogJ6W/SZpCbk0EEOA8xAsXYm"
    }

    response = client.get("/auth/login?nexturl=%2Frosalution&ticket=FakeTicketString")

    assert response.url == "http://dev.cgds.uab.edu/rosalution"

def test_local_logout(client):
    """ This tests functionality of the local logout function """
    response = client.get(
        "/auth/logout",
        cookies={
            "session": create_session_cookie({
                "username": "UABProvider",
                "local": True
            })
        }
    )

    assert response.json() == {"access_token": ""}

def test_prod_logout(client):
    """ This tests functionality if the user logs out after logging in with their BlazerId """
    response = client.get(
        '/auth/logout',
        headers={
            "host": 'dev.cgds.uab.edu'
        },
        cookies={
            "session": create_session_cookie({
                "username": "UABProvider",
                "local": False
            })
        }
    )

    assert response.json() == {'url':
        'https://padlockdev.idm.uab.edu/cas/logout?' +
        'service=http%3A%2F%2Fdev.cgds.uab.edu%2Frosalution%2Fapi%2Fauth%2Flogout_callback'
    }

def test_logout_callback(client):
    """
    This gets called when the CAS logout calls back after destroying the BlazerId session
    and redirects the user to login
    """

    response = client.get('/auth/logout_callback', allow_redirects=False)

    assert response.status_code == 307
    assert response.headers['location'] == 'http://dev.cgds.uab.edu/rosalution/login'
