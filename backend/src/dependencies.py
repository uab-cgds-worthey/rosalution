""" FastAPI application dependencies that are shared within the entire application """
from fastapi import Request

from .core.annotation import AnnotationQueue


def get_db(request: Request) -> dict:
    """Return the database instance stored in the application state."""
    return request.app.state.database()


# Queue that processess annotation tasks safely between threads
annotation_queue = AnnotationQueue()
