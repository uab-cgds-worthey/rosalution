"""
End points for backend
"""
import os
import json

from typing import List, Optional
from cas import CASClient

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware

from .core.analysis import Analysis, AnalysisSummary

DESCRIPTION = """
diverGen REST API assists researchers study 🧬 variation in patients 🧑🏾‍🤝‍🧑🏼 
by helping select candidate animal models 🐀🐁🐠🪱 to replicate the variation
to further research to dervice a diagnose and provide therapies for
ultra-rare diseases.
"""

cas_client = CASClient(
    version=3,
    service_url='http://dev.cgds.uab.edu/divergen/api/login?nexturl=%2Fdivergen',
    server_url='https://padlockdev.idm.uab.edu/cas/'
)

tags_metadata = [{
    "name": "analysis",
    "description": "Analyses of cases with information such as target gene, variation, phenotyping, and more."
}, {
    "name": "lifecycle",
    "description": "Heart-beat that external services use to verify if the application is running."
}]

## CORS Policy ##

origins = [
    "http://dev.cgds.uab.edu",
    "https://padlockdev.idm.uab.edu"
]

app = FastAPI(
    title="diverGen API",
    description=DESCRIPTION,
    openapi_tags=tags_metadata,
    root_path="/divergen/api/"
)

app.add_middleware(SessionMiddleware, secret_key="!secret")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    """ Returns a summary of every analysis within the application """
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
    """ Returns analysis by searching for id """
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
    """ Returns analysis case data by calling method to find case by it's name """
    if name == 'CPAM0002':
        return find_analysis_by_name("CPAM0002")
    if name == 'CPAM0046':
        return find_analysis_by_name("CPAM0046")
    if name == 'CPAM0053':
        return find_analysis_by_name("CPAM0053")
    raise HTTPException(status_code=404, detail="Item not found")

@app.get('/heart-beat', tags=["lifecycle"])
async def heartbeat():
    """ Returns a heart-beat that orchestration services can use to determine if the application is running """
    return "thump-thump"

# pylint: disable=no-member
# This is done because pylint doesn't appear to be recognizing python-cas's functions saying they have no member
@app.get('/login')
async def login(request: Request, nexturl: Optional[str] = None, ticket: Optional[str] = None):
    """ diverGen Login Method """
    if request.session.get("username", None):
        # We're already logged in, don't need to do the login process
        print("We are already logged in as: %s", request.session.get("user", None))
        return {'url': 'http://dev.cgds.uab.edu/divergen/'}

    if not ticket:
        # No ticket, the request comes from end user, send to CAS login
        cas_login_url = cas_client.get_login_url()
        return {'url': cas_login_url}

    user, attributes, pgtiou = cas_client.verify_ticket(ticket)

    print('CAS verify ticket response: user: %s, attributes: %s, pgtiou: %s', user, attributes, pgtiou)

    if not user:
        # Failed ticket verification, this should be an error page of some kind maybe?
        return {'url': 'http://dev.cgds.uab.edu/divergen/login'}

    # Login was successful, redirect to the 'nexturl' query parameter
    request.session['username'] = user
    base_url = 'http://dev.cgds.uab.edu'
    return RedirectResponse(base_url + nexturl)

@app.get('/get_user')
def get_user(request: Request):
    """ Returns active user in session """
    if 'username' in request.session:
        return {'username': request.session['username']}

    return {'username': ''}

@app.get('/logout')
def logout(request: Request):
    """ Test Logout Method """
    redirect_url = request.url_for('login')
    cas_logout_url = cas_client.get_logout_url(redirect_url)
    print('CAS logout URL: %s', cas_logout_url)
    request.session.pop("username", None)
    return {'url': cas_logout_url}
