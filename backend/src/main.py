"""
End points for backend
"""
import os
import json
from typing import List

from fastapi import FastAPI, HTTPException

from .core.analysis import Analysis, AnalysisSummary

DESCRIPTION = """
diverGen REST API assists researchers study 🧬 variation in patients 🧑🏾‍🤝‍🧑🏼 
by helping select candidate animal models 🐀🐁🐠🪱 to replicate the variation
to further research to dervice a diagnose and provide therapies for
ultra-rare diseases.
"""

tags_metadata = [{
    "name": "analysis",
    "description": "Analyses of cases with information such as target gene, variation, phenotyping, and more."
}, {
    "name": "lifecycle",
    "description": "Heart-beat that external services use to verify if the application is running."
}]

app = FastAPI(
    title="diverGen API",
    description=DESCRIPTION,
    openapi_tags=tags_metadata,
    root_path="/divergen/api/"
)

## diverGen endpoints

@app.get('/analysis', response_model=List[Analysis], tags=["analysis"])
async def get_all_analyses():
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

@app.get('/analysis/summary', response_model=List[AnalysisSummary], tags=["analysis"])
async def get_all_analyses_summaries():
    """ Returns a summary of every analysis within the application"""
    # This is necessary for pytest to get relative pathing.
    # Better variable names need to be devised.
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    path_to_file = os.path.join(current_directory, "../fixtures/analyses-summary.json")
    with open(path_to_file, mode='r', encoding='utf-8') as file_to_open:
        data = json.load(file_to_open)
        file_to_open.close()

    return data


def find_analysis_by_name(name: str):
    """ Returns analysis by searching for id"""
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    path_to_file = os.path.join(current_directory, "../fixtures/analyses.json")
    with open(path_to_file, mode='r', encoding='utf-8') as file_to_open:
        analyses = json.load(file_to_open)
        file_to_open.close()
    for analysis in analyses:
        analysis_name = analysis.get('name')
        if analysis_name == name:
            return analysis

    return None

@app.get('/analysis/{name}', response_model=Analysis, tags=["analysis"])
async def get_analysis_by_name(name: str):
    """ Returns analysis case data by calling method to find case by it's name"""
    if name == 'CPAM0002':
        return find_analysis_by_name("CPAM0002")
    if name == 'CPAM0046':
        return find_analysis_by_name("CPAM0046")
    if name == 'CPAM0053':
        return find_analysis_by_name("CPAM0053")
    raise HTTPException(status_code=404, detail="Item not found")


@app.get('/heart-beat', tags=["lifecycle"])
async def heartbeat():
    """ Returns a heart-beat that orchestration services can use to determine if the application is running"""
    return "thump-thump"
