"""
End points for backend
"""
import os
import json

from typing import List, Optional
from cas import CASClient

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
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
    service_url='http://dev.cgds.uab.edu/divergen/api/login?nexturl=/divergen',
    server_url='http://padlockdev.idm.uab.edu/cas/login'
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
    "http://padlockdev.idm.uab.edu"
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
@app.get('/loginold', tags=["authentication"])
async def login(request: Request, nexturl: Optional[str] = None, ticket: Optional[str] = None):
    """ Test Login Method """
    if request.session.get("user", None):
        # Already logged in
        return RedirectResponse(request.url_for('divergen'))

    if not ticket:
        cas_login_url = cas_client.get_login_url()
        print('CAS login URL: %s', cas_login_url)
        return RedirectResponse(cas_login_url)

    # There is a ticket, the request come from CAS as callback.
    # need call `verify_ticket()` to validate ticket and get user profile.
    print('ticket: %s', ticket)
    print('nextURL: %s', nexturl)

    user, attributes, pgtiou = cas_client.verify_ticket(ticket)

    print('CAS verify ticket response: user: %s, attributes: %s, pgtiou: %s', user, attributes, pgtiou)

    if not user:
        return HTMLResponse('Failed to verify ticket. <a href="/login">Login</a>')

    # Login successfully, redirect according `nexturl` query parameter.
    response = RedirectResponse(nexturl)
    request.session['user'] = dict(user=user)
    return response

@app.get('/login')
async def logintest(request: Request, nexturl: Optional[str] = None, ticket: Optional[str] = None):
    """ Test Login Test Method """
    print("This is happening: #1")
    print('Ticket: ', ticket)
    print('Next URL: ', nexturl)
    if request.session.get("user", None):
        # We're already logged in, don't need to do the login process
        print("We are already logged in as: %s", request.session.get("user", None))
        return {'url': nexturl}

    print("This is happening: #2")

    if not ticket:
        cas_login_url = cas_client.get_login_url()
        return {'url': cas_login_url}

    print("This is happening: #3")

    user, attributes, pgtiou = cas_client.verify_ticket(ticket)

    print('CAS verify ticket response: user: %s, attributes: %s, pgtiou: %s', user, attributes, pgtiou)

    if not user:
        # This should be an error page of some kind
        return {'url': 'http://dev.cgds.uab.edu/divergen/login'}

    print("This is happening: #4")

    # Login was successful, redirect to the 'nexturl' query parameter
    request.session['username'] = user
    print("This is happening: #5")
    url_prefix = 'http://dev.cgds.uab.edu/divergen/api/login'
    url_full = url_prefix + nexturl
    # return {'username': request.session.get("user", None)}
    return {'url': url_full}

@app.get('/validate')
async def validatetest(request: Request, nexturl: Optional[str] = None, ticket: Optional[str] = None):
    """ Test Validate Test Method """
    request.session['username'] = 'FastAPI'
    print(request.session)
    print(request.session.get("username", None))
    print('Ticket: ', ticket)
    print('Next URL: ', nexturl)
    user = request.session.get('username', None)
    return {'username': user}

@app.get('/test')
async def testtest(request: Request):
    """ Test Test Test Method """
    request.session.pop('username', None)
    print(request.session)
    return {}

@app.get('/logout')
def logout(request: Request):
    """ Test Logout Method """
    redirect_url = request.url_for('logout_callback')
    cas_logout_url = cas_client.get_logout_url(redirect_url)
    print('CAS logout URL: %s', cas_logout_url)
    return {'url': cas_logout_url}

@app.get('/logout_callback')
def logout_callback(request: Request):
    """ Test Logout Callback Method """
    # redirect from CAS logout request after CAS logout successfully
    # response.delete_cookie('username')
    request.session.pop("user", None)
    return RedirectResponse("http://dev.cgds.uab.edu/divergen/login")
