"""
End points for backend
"""
import logging
import logging.config

from os import path

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from .routers import analysis_router, annotation_router, auth_router

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
        "description":
            ("Temporary endpoint to facilitate annotating an analysis from a default annotation configuration"),
    },
    {
        "name": "lifecycle",
        "description": "Heart-beat that external services use to verify if the application is running.",
    },
    {
        "name": "auth",
        "description": "Handles user authentication",
    },
]

## CORS Policy ##
origins = ["http://dev.cgds.uab.edu", "https://padlockdev.idm.uab.edu"]

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)

# create logger
logger = logging.getLogger(__name__)

app = FastAPI(
    title="rosalution API",
    description=DESCRIPTION,
    openapi_tags=tags_metadata,
    root_path="/rosalution/api/"
)

app.include_router(analysis_router.router)
app.include_router(annotation_router.router)
app.include_router(auth_router.router)

if __debug__:
    from .routers import dev_router
    app.include_router(dev_router.router)

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

    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warn message')
    logger.error('error message')
    logger.critical('critical message')

    
    return "thump-thump"

@app.get("/test", tags=["lifecycle"])
def test():
    logger.debug('debug message')
    return "test"