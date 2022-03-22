"""
End points provided by Fast-API
"""
import os
import json

from fastapi import FastAPI, HTTPException

app = FastAPI()

## Real diverGen prototype endpoints

@app.get('/analysis')
async def get_analysis_listing():
    """ Returns every analysis available"""
    # This is necessary for pytest to get relative pathing.
    # Better variable names need to be devised.
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    path_to_file = os.path.join(current_directory, "../models/analyses.json")
    # file_to_open = open(path_to_file, mode = 'r', encoding = 'utf-8')
    with open(path_to_file, mode = 'r', encoding = 'utf-8') as file_to_open:
        data = json.load(file_to_open)
        file_to_open.close()

    return data

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

@app.get('/cat')
async def pet_cat():
    """ Meow """
    return "=^.^= Meow"
