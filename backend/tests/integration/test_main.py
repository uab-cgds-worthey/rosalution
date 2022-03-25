"""Our integration test file"""
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

## Tests for diverGen endpoints

def test_get_analysis_listing():
    """Testing that the correct number of analyses were returned and in the right order"""
    response = client.get('/analysis')
    assert response.status_code == 200
    assert len(response.json()) == 4
    assert response.json()[2]['name'] == 'CPAM0053'

## Tests for helper endpoints

def test_read_main():
    """Ensures Hello World is returned"""
    response = client.get("/default")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
