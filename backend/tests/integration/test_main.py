"""Endpoint Integration for Analysis Routes"""
import json 
from base64 import b64encode
from cas import CASClient

from fastapi.testclient import TestClient
from itsdangerous import TimestampSigner

from src.main import app

client = TestClient(app)

## Helper functions

def create_session_cookie(data) -> str:
    signer = TimestampSigner(str('!secret'))

    return signer.sign(b64encode(json.dumps(data).encode('utf-8')),).decode('utf-8')

## Tests for diverGen endpoints

def test_get_analyses():
    """Testing that the correct number of analyses were returned and in the right order"""
    response = client.get('/analysis')
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[2]['name'] == 'CPAM0053'

def test_get_analysis_summary():
    """Testing if the analysis summary endpoint returns all of the analyses available"""
    response = client.get('/analysis/summary')
    assert len(response.json()) == 5

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
    cas_client = CASClient(
        version=3,
        service_url='http://dev.cgds.uab.edu/divergen/api/login?nexturl=%2Fdivergen',
        server_url='https://padlockdev.idm.uab.edu/cas/'
    )

    def mockVerifyReturn():
        return '<cas:serviceresponse xmlns:cas="http://www.yale.edy/tp/cas"> \
                    <cas:authenticationsuccess> \
                        <cas:user>UABProvider</cas:user> \
                    </cas:authenticationsuccess> \
                </cas:serviceresponse>"'
    
    monkeypatch.setattr(cas_client, "verify_ticket", mockVerifyReturn)

    response = client.get('/login?nexturl=%2Fdivergen&ticket=ST-1651606388-USIl7oNSThX5ET5oV6pMvnZNGKbTNBbE')

    print(response.json())

# def test_login_existing_session_not_valid_user():