from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == { "Hello": "World" }

def test_get_fruit_apple():
    response = client.get("/fruit/1")
    assert response.status_code == 200
    assert response.json() == { "fruit": "apple" }

def test_get_fruit_fail():
    response = client.get("/fruit/4")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Fruit ID not found'}

def test_items_query():
    response = client.get("/items/5?q=somequery")
    resJson = response.json()
    assert response.status_code == 200
    assert resJson["q"] == "somequery"
    assert resJson["item_id"] == 5

def test_pet_cat():
    response = client.get('/cat')
    assert response.status_code == 200
    assert response.json() == "=^.^= Meow"