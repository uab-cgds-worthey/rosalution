"""
End points for backend
"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/default")
def read_root():
    """Returns Hello World"""
    return {"Hello": "World"}
