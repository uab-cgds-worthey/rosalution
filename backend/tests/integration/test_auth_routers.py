"""Authentication Routes Intergration test"""
from cas import CASClient
import pytest


# Authentication Tests #
@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories")
async def test_login_no_session(client):
    """Testing the login endpoint when there is no login session already"""
    response = await client.get("/auth/login")
    assert (
        response.json()["url"] == "https://fake.uab.cas/cas/login?service=http%3A" +
        "%2F%2Ffake.cgds.uab.edu%2Frosalution%2Fapi%2Fauth%2Flogin%3Fnexturl%3D%252F"
    )


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories")
async def test_login_successful(client, cas_client: CASClient, monkeypatch):
    """Testing the login endpoint when there's a successful login and redirect"""

    # This unused parameter is required for the monkeypatch to successfully use the mock verify function,
    # if no empty paramter is provided then the tests will crash.
    def mock_verify_return(paramater):  #pylint: disable=unused-argument
        return ('developer', 'unused_attributes', 'unused_pgtiou')

    monkeypatch.setattr(cas_client, "verify_ticket", mock_verify_return)

    response = await client.get("/auth/login?nexturl=%2F&ticket=FakeTicketString")

    assert response.status_code == 307
    assert response.url == "http://test/auth/login?nexturl=%2F&ticket=FakeTicketString"


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories", "mock_settings_cas_disabled")
async def test_logout(client):
    """ This tests functionality of the local logout function """
    response = await client.get("/auth/logout",)

    assert response.json() == {"access_token": ""}


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_settings")
async def test_cas_enabled_logout(client):  # pylint: disable=unused-argument
    """ This tests functionality if the user logs out after logging in with their BlazerId """
    response = await client.get(
        '/auth/logout',
        headers={"host": 'dev.cgds.uab.edu'},
    )

    assert response.json() == {
        'url':
            'https://fake.uab.cas/cas/logout?' +
            'service=http%3A%2F%2Fdev.cgds.uab.edu%2Frosalution%2Fapi%2Fauth%2Flogout_callback'
    }


@pytest.mark.anyio
async def test_logout_callback(client):
    """
    This gets called when the CAS logout calls back after destroying the BlazerId session
    and redirects the user to login
    """

    response = await client.get('/auth/logout_callback', follow_redirects=False)

    assert response.status_code == 307
    assert response.headers['location'] == 'http://api.fake.cgds.uab.edu/login'
