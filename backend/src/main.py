"""
End points for backend
"""
import os
import json
import uvicorn

from fastapi import FastAPI

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


@app.get('/analysis/CPAM0002')
async def get_analysis_by_id():
    """ Returns analysis by id"""
    # This is necessary for pytest to get relative pathing.
    # Better variable names need to be devised.
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    path_to_file = os.path.join(current_directory, "../fixtures/analysis-data.json")
    with open(path_to_file, mode='r', encoding='utf-8') as file_to_open:
        analyses = json.load(file_to_open)
        file_to_open.close()
    
    for analysis in analyses:
        analysis_id = analysis.get('id')
        if(analysis_id == "160d1134-784d-42f0-a839-7a88ea26f530"):
            # Finding Case CPAM0053
            result = analysis
            break

    return result


@app.get('/analysis/CPAM0046')
async def get_analysis_by_id():
    """ Returns analysis by id"""
    # This is necessary for pytest to get relative pathing.
    # Better variable names need to be devised.
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    path_to_file = os.path.join(current_directory, "../fixtures/analysis-data.json")
    with open(path_to_file, mode='r', encoding='utf-8') as file_to_open:
        analyses = json.load(file_to_open)
        file_to_open.close()
    
    for analysis in analyses:
        analysis_id = analysis.get('id')
        if(analysis_id == "10f7aa04-6adf-4538-a700-ebe2f519473f"):
            # Finding Case CPAM0053
            result = analysis
            break

    return result


@app.get('/analysis/CPAM0053')
async def get_analysis_by_id():
    """ Returns analysis by id"""
    # This is necessary for pytest to get relative pathing.
    # Better variable names need to be devised.
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    path_to_file = os.path.join(current_directory, "../fixtures/analysis-data.json")
    with open(path_to_file, mode='r', encoding='utf-8') as file_to_open:
        analyses = json.load(file_to_open)
        file_to_open.close()
    
    for analysis in analyses:
        analysis_id = analysis.get('id')
        if(analysis_id == "10342gs4-6adf-4538-a700-ebef319473f"):
            # Finding Case CPAM0053
            result = analysis
            break

    return result

## Test endpoints

@app.get("/default")
def read_root():
    """Returns Hello World"""
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
