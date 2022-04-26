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
    path_to_file = os.path.join(current_directory, "../fixtures/analyses.json")
    with open(path_to_file, mode='r', encoding='utf-8') as file_to_open:
        data = json.load(file_to_open)
        file_to_open.close()

    return data

def find_analysis_by_name(name: str):
    """ Returns analysis by searching for id"""
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    path_to_file = os.path.join(current_directory, "../fixtures/analysis-data.json")
    with open(path_to_file, mode='r', encoding='utf-8') as file_to_open:
        analyses = json.load(file_to_open)
        file_to_open.close()
    for analysis in analyses:
        analysis_name = analysis.get('name')
        if analysis_name == name:
            return analysis

    return None

@app.get('/analysis/{name}')
async def get_analysis_by_name(name: str):
    """ Returns analysis case data by calling method to find case by it's name"""
    if name == 'CPAM0002':
        return find_analysis_by_name("CPAM0002")
    if name == 'CPAM0046':
        return find_analysis_by_name("CPAM0046")
    if name == 'CPAM0053':
        return find_analysis_by_name("CPAM0053")
    raise HTTPException(status_code=404, detail="Item not found")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
