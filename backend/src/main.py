"""
End points for backend
"""

from contextlib import asynccontextmanager
import json
import logging
import logging.config
from os import path
from pathlib import Path
import urllib3

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pymongo import AsyncMongoClient
from pymongo.errors import ConnectionFailure
import gridfs

from .database import Database

from .config import get_settings
from .profiler_middleware import register_profiler_middleware
from .routers import analysis_router, annotation_router, auth_router, project_router

urllib3.disable_warnings()

DESCRIPTION = """
rosalution REST API assists researchers study 🧬 variation in patients 🧑🏾‍🤝‍🧑🏼
by helping select candidate animal models 🐀🐁🐠🪱 to replicate the variation
to further research to dervice a diagnose and provide therapies for
ultra-rare diseases.
"""

tags_metadata = [
    {
        "name": "project",
        "description": "Projects the user is a tenant of.",
    },
    {
        "name": "analysis",
        "description": "Analyses of cases with information such as target gene, variation, phenotyping, and more.",
    },
    {
        "name": "analysis sections",
        "description": "Adds, updates, and removes content from an Analysis Section's fields within an analysis.",
    },
    {
        "name": "analysis discussions",
        "description": "Adds, updates, and removes discussion messages from an Analysis.",
    },
    {
        "name": "analysis attachments",
        "description": "Adds, updates, and removes attachments from an Analysis.",
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

log_file_path = path.join(path.dirname(path.abspath(__file__)), "../logging.conf")
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)

# create logger
logger = logging.getLogger("uvicorn.error")
logger.info("Configured application logging level: %s", logging.getLevelName(logger.level))

settings = get_settings()

## OAuth Token ##

@asynccontextmanager
async def db_lifespan(application: FastAPI):
    """Application lifespan context manager that initializes resources during startup and cleans up on shutdown."""

    """
    Verifies required ROSALUTION_KEY environment variable set with descriptive error at start of service.
    """
    if None == settings.rosalution_key:
        raise ValueError('Environment variable "ROSALUTION_KEY" missing. App requires secret for secure encoding.')

    ## Database ##
    mongodb_connection_uri = f"mongodb://{settings.mongodb_host}/{settings.mongodb_db}"
    async with AsyncMongoClient(mongodb_connection_uri) as mongodb_async_client:
        bucket = gridfs.asynchronous.AsyncGridFS(mongodb_async_client.rosalution_db)
        database = Database(mongodb_async_client, bucket)
        logger.info("Attemping Database Connection...")
        try:
            await database.ping()
        except ConnectionFailure as error:
            logger.error("Problem connecting to database cluster.")
            raise error

        application.state.database = database
        logger.info("Connceted to database cluster")
        yield

app = FastAPI(
    title="rosalution API",
    description=DESCRIPTION,
    openapi_tags=tags_metadata,
    root_path="/rosalution/api/",
    lifespan=db_lifespan
)

app.include_router(analysis_router.router)
app.include_router(annotation_router.router)
app.include_router(auth_router.router)
app.include_router(project_router.router)

if __debug__:
    from .routers import dev_router

    app.include_router(dev_router.router)

## CORS Policy ##
origins = [settings.origin_domain_url, settings.cas_server_url]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

register_profiler_middleware(app, settings.profiler_enabled, settings.profiler_renderer)


@app.get("/render-layout/annotations", tags=["config"])
def get_annotations_render_layout():
    """
    Returns the configurable render layout for the annotations. The configuration is read from a file each time
    the endpoint is called.
    """
    render_layout = []
    with open(
        Path(__file__).resolve().parent / "../annotation-render-layout.json", mode="r", encoding="utf-8"
    ) as layout_file:
        render_layout = json.load(layout_file)
    return render_layout


@app.get("/heart-beat", tags=["lifecycle"])
def heartbeat():
    """Returns a heart-beat that orchestration services can use to determine if the application is running"""

    return "thump-thump"
