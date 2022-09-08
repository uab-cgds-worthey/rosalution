"""
End points for backend
"""
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI

from starlette.middleware.sessions import SessionMiddleware

from .routers import analysis_router, annotation_router, auth_router

from .dependencies import database, annotation_queue

DESCRIPTION = """
rosalution REST API assists researchers study 🧬 variation in patients 🧑🏾‍🤝‍🧑🏼
by helping select candidate animal models 🐀🐁🐠🪱 to replicate the variation
to further research to dervice a diagnose and provide therapies for
ultra-rare diseases.
"""

tags_metadata = [
    {
        "name": "analysis",
        "description": "Analyses of cases with information such as target gene, variation, phenotyping, and more.",
    },
    {
        "name": "annotation",
        "description": (
            "Temporary endpoint to facilitate annotating an analysis from a default annotation configuration"
        ),
    },
    {
        "name": "lifecycle",
        "description": "Heart-beat that external services use to verify if the application is running.",
    },
    {"name": "auth", "description": "Handles user authentication"},
]

## CORS Policy ##
origins = ["http://dev.cgds.uab.edu", "https://padlockdev.idm.uab.edu"]

app = FastAPI(
    title="rosalution API",
    description=DESCRIPTION,
    openapi_tags=tags_metadata,
    root_path="/rosalution/api/",
)

app.include_router(analysis_router.router, dependencies=[Depends(database)])
app.include_router(annotation_router.router, dependencies=[Depends(database), Depends(annotation_queue)])
app.include_router(auth_router.router)

app.add_middleware(SessionMiddleware, secret_key="!secret")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/heart-beat", tags=["lifecycle"])
def heartbeat():
    """Returns a heart-beat that orchestration services can use to determine if the application is running"""
    return "thump-thump"
