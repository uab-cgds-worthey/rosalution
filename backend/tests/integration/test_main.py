"""Endpoint Integration for Analysis Routes"""
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

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
