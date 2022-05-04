"""
End points for backend
"""
<<<<<<< HEAD
import os
import json

from typing import List, Optional
from cas import CASClient
=======
from typing import List
>>>>>>> Work in progress for annotation code base

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware

from .core.analysis import Analysis, AnalysisSummary
from .repository.analysis_collection import AnalysisCollection

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

analysis_collection = AnalysisCollection()

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
    return analysis_collection.all()


@app.get('/analysis/summary',
         response_model=List[AnalysisSummary], tags=["analysis"])
async def get_all_analyses_summaries():
    """ Returns a summary of every analysis within the application"""
    return analysis_collection.all_summaries()


@app.get('/analysis/{name}', response_model=Analysis, tags=["analysis"])
async def get_analysis_by_name(name: str):
    """ Returns analysis case data by calling method to find case by it's name """
    if name == 'CPAM0002':
        return analysis_collection.find_by_name('CPAM0002')
    if name == 'CPAM0046':
        return analysis_collection.find_by_name('CPAM0046')
    if name == 'CPAM0053':
        return analysis_collection.find_by_name('CPAM0053')

<<<<<<< HEAD
=======
    raise HTTPException(status_code=404, detail="Item not found")

<<<<<<< HEAD
>>>>>>> Work in progress for annotation code base
=======

>>>>>>> Work in progress to queue annotation tasks according to the dataset configuration
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
        return {'url': 'http://dev.cgds.uab.edu/divergen/'}

    if not ticket:
        # No ticket, the request comes from end user, send to CAS login
        cas_login_url = cas_client.get_login_url()
        return {'url': cas_login_url}

    user, attributes, pgtiou = cas_client.verify_ticket(ticket)

    if not user:
        # Failed ticket verification, this should be an error page of some kind maybe?
        return RedirectResponse('http://dev.cgds.uab.edu/divergen/login')

    # Login was successful, redirect to the 'nexturl' query parameter
    request.session['username'] = user
    request.session['attributes'] = attributes
    request.session['pgtiou'] = pgtiou
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
    request.session.pop("username", None)
    request.session.pop("attributes", None)
    request.session.pop("pgtiou", None)

    return {'url': cas_logout_url}
