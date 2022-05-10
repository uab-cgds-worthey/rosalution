"""
End points for backend
"""
from typing import List, Optional
from cas import CASClient
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi import Depends, FastAPI, HTTPException, status

from .core.analysis import Analysis, AnalysisSummary
from .database import Database

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
    "name": "annotation",
    "description": "Temporary endpoint to facilitate annotating an analysis from a default annotation configuration"
}, {
    "name": "lifecycle",
    "description": "Heart-beat that external services use to verify if the application is running."
}]

## CORS Policy ##

origins = [
    "http://dev.cgds.uab.edu",
    "https://padlockdev.idm.uab.edu"
]

# database_client = FunctionCallToMakeDatabase()
fakeClientReplaceWithReal = {}
database = Database(fakeClientReplaceWithReal)

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

@app.get('/analysis', response_model=List[Analysis], tags=["analysis"], )
def get_all_analyses(collections = Depends(database)):
    """ Returns every analysis available"""
    return collections['analysis'].all()


@app.get('/analysis/summary',
         response_model=List[AnalysisSummary], tags=["analysis"])
def get_all_analyses_summaries(collections = Depends(database)):
    """ Returns a summary of every analysis within the application"""
    return collections['analysis'].all_summaries()


@app.get('/analysis/{name}', response_model=Analysis, tags=["analysis"])
def get_analysis_by_name(name: str, collections = Depends(database)):
    """ Returns analysis case data by calling method to find case by it's name"""
    if name == 'CPAM0002':
        return collections['analysis'].find_by_name('CPAM0002')
    if name == 'CPAM0046':
        return collections['analysis'].find_by_name('CPAM0046')
    if name == 'CPAM0053':
        return collections['analysis'].find_by_name('CPAM0053')

    raise HTTPException(status_code=404, detail="Item not found")

@app.post('/annotate/{name}', status_code=status.HTTP_202_ACCEPTED)
def annotate_analysis(name: str):
    return {"name": name}

@app.get('/heart-beat', tags=["lifecycle"])
def heartbeat():
    """ Returns a heart-beat that orchestration services can use to determine if the application is running"""
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
