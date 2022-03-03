from fastapi import FastAPI, HTTPException

app = FastAPI()

fake_db = {}
fake_db[1] = "apple"
fake_db[2] = "banana"
fake_db[3] = "orange"

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/fruit/{fruit_id}")
async def get_fruit(fruit_id: int):
    if fruit_id in fake_db:
        return {"fruit": fake_db[fruit_id]}
    raise HTTPException(status_code=404, detail="Fruit ID not found")
    
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get('/cat')
async def pet_cat():
    return "=^.^= Meow"