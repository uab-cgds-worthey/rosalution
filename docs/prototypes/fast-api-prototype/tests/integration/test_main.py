"""Our integration test file"""
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

## Tests for helper endpoints to show how to test FastAPI endpoints


def test_read_main():
    """Ensures Hello World is returned"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_get_fruit_apple():
    """Ensures apple is returned in a json object"""
    response = client.get("/fruit/1")
    assert response.status_code == 200
    assert response.json() == {"fruit": "apple"}


def test_get_fruit_fail():
    """Tests a failure with the fruit endpoint"""
    response = client.get("/fruit/4")
    assert response.status_code == 404
    assert response.json() == {"detail": "Fruit ID not found"}


def test_items_query():
    """Tests that an item id and query are accepted and returned"""
    response = client.get("/items/5?query=somequery")
    json_response = response.json()
    assert response.status_code == 200
    assert json_response["query"] == "somequery"
    assert json_response["item_id"] == 5


def test_pet_cat():
    """You know what this does, don't you?"""
    response = client.get("/cat")
    assert response.status_code == 200
    assert response.json() == "=^.^= Meow"
