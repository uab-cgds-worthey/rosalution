""" FastAPI application dependencies that are shared within the entire application """
# pylint: disable=too-few-public-methods
# Disabling too few public metods due to utilizing Pydantic/FastAPI BaseSettings class
import gridfs
from pymongo import MongoClient
from fastapi.security import OAuth2PasswordBearer

from .core.annotation import AnnotationQueue
from .database import Database
from .config import get_settings

settings = get_settings()
mongodb_connection_uri = f"mongodb://{settings.mongodb_host}/{settings.mongodb_db}"
mongodb_client = MongoClient(mongodb_connection_uri)
bucket = gridfs.GridFS(mongodb_client.rosalution_db)

# Database/Repositories
database = Database(mongodb_client, bucket)

# Queue that processess annotation tasks safely between threads
annotation_queue = AnnotationQueue()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.openapi_api_token_route)
