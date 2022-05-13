""" FastAPI application dependencies that are shared within the entire application """

from .annotation import AnnotationQueue
from .database import Database

# Database/Repositories
fake_mongodb_client = {}
database = Database(fake_mongodb_client)

# Queue that processess annotation tasks safely between threads
annotation_queue = AnnotationQueue()
