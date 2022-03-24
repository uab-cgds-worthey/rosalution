"""
End points for backend
"""
import os
import json
import uvicorn

from fastapi import FastAPI, HTTPException

app = FastAPI()

## diverGen endpoints

@app.get('/analysis')
async def get_analysis_listing():
    """ Returns every analysis available"""
    # This is necessary for pytest to get relative pathing.
    # Better variable names need to be devised.
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    path_to_file = os.path.join(current_directory, "../models/analyses.json")
    with open(path_to_file, mode='r', encoding='utf-8') as file_to_open:
        data = json.load(file_to_open)
        file_to_open.close()

    return data

## Test endpoints

@app.get("/default")
def read_root():
    """Returns Hello World"""
    return {"Hello": "World"}
