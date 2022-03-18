"""
End points for backend
"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_frothers():
    """Returns Hello World"""
    return {"Hello": "World"}
