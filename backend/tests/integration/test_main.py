"""Our integration test file"""
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

def test_read_main():
    """Ensures Hello World is returned"""
    response = client.get("/default")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
