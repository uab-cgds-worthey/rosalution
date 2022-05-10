"""Endpoint Integration for Analysis Routes"""
import json
from base64 import b64encode
from cas import CASClient
from unittest.mock import Mock
import pytest

from fastapi.testclient import TestClient
from itsdangerous import TimestampSigner

from src.main import app
from src.database import Database


## Helper functions

def create_session_cookie(data) -> str:
    """ Function that creates a fake session token cookie to mimic Starlette session middleware """
    signer = TimestampSigner(str('!secret'))

    return signer.sign(b64encode(json.dumps(data).encode('utf-8')),).decode('utf-8')

## Tests for diverGen endpoints ##

# Analyses Tests #

def test_get_analyses(client, mock_database_collections):
    """Testing that the correct number of analyses were returned and in the right order"""
    ## Future Database Mock Example 
    ## mock_database_collections.db['analysis'].find()
    ## mock_database_collections.db['analysis'].find.return_value = JSON Fixture

    response = client.get('/analysis')
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[2]['name'] == 'CPAM0053'

def test_get_analysis_summary(client):
    """Testing if the analysis summary endpoint returns all of the analyses available"""
    response = client.get('/analysis/summary')
    assert len(response.json()) == 5

# Authentication Tests #

def test_login_no_session():
    """ Testing the login endpoint when there is no login session already """
    response = client.get('/login')
    assert response.json()['url'] == 'https://padlockdev.idm.uab.edu/cas/login?service=http%3A' + \
                                     '%2F%2Fdev.cgds.uab.edu%2Fdivergen%2Fapi%2Flogin%3Fnexturl%3D%252Fdivergen'

def test_login_existing_session():
    """ Testing the login endpoint when there is an existing login session """
    response = client.get('/login', cookies={'session': create_session_cookie({'username': 'UABProvider'})})
    assert response.json()['url'] == 'http://dev.cgds.uab.edu/divergen/'

def test_login_successful(monkeypatch):
    """ Testing the login endpoint when there's a successful login and redirect """
    cas_client = CASClient(
        version=3,
        service_url='http://fake.url/login',
        server_url='https://fake.url/cas/'
    )

    def mock_verify_return():
        return '<cas:serviceresponse xmlns:cas="http://www.yale.edy/tp/cas"> \
                    <cas:authenticationsuccess> \
                        <cas:user>UABProvider</cas:user> \
                    </cas:authenticationsuccess> \
                </cas:serviceresponse>"'

    monkeypatch.setattr(cas_client, "verify_ticket", mock_verify_return)

    response = client.get('/login?nexturl=%2Fdivergen&ticket=FakeTicketString')

    assert response.url == 'http://dev.cgds.uab.edu/divergen/login'

def test_get_user_not_logged_in():
    """ Testing the get_user endpoint when there is no user saved in the session """
    response = client.get('/get_user')
    assert response.json()['username'] == ''

def test_get_user_logged_in():
    """ Testing if the logged in user returns the proper username """
    response = client.get('/get_user', cookies={'session': create_session_cookie({'username': 'UABProvider'})})
    assert response.json()['username'] == 'UABProvider'

def test_logout():
    """ Testing the log out functionality """
    response = client.get('/logout')
    assert response.json()['url'] == 'https://padlockdev.idm.uab.edu/cas/logout?' \
                                     'service=http%3A%2F%2Ftestserver%2Fdivergen%2Fapi%2Flogin'
@pytest.fixture(name='client', scope='class')
def test_application_client():
    return TestClient(app)

@pytest.fixture(scope='class')
def mock_database_collections():
    database_client = Mock()
    database_client.db = {
        'analysis': Mock(),
        'annotations': Mock()
    }
    fake_database = Database(database_client)
    app.dependency_overrides['database'] = fake_database
    yield database_client.db
    app.dependency_overrides.clear()
