"""
End points provided by Fast-API
"""
import uvicorn

from fastapi import FastAPI, HTTPException

app = FastAPI()

## Helper endpoints to show how FastAPI works

fake_db = {}
fake_db[1] = "apple"
fake_db[2] = "banana"
fake_db[3] = "orange"


@app.get("/")
def read_root():
    """Returns Hello World"""
    return {"Hello": "World"}


@app.get("/fruit/{fruit_id}")
async def get_fruit(fruit_id: int):
    """Accepts an int and returns a json object with fruit and fruit name"""
    if fruit_id in fake_db:
        return {"fruit": fake_db[fruit_id]}
    raise HTTPException(status_code=404, detail="Fruit ID not found")


@app.get("/items/{item_id}")
async def read_item(item_id: int, query: str = None):
    """
    Accepts an item int and/or a query
    Returns a json object with item id and/or query
    """
    return {"item_id": item_id, "query": query}


@app.get("/cat")
async def pet_cat():
    """Meow"""
    return "=^.^= Meow"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
