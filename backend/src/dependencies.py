""" FastAPI application dependencies that are shared within the entire application """
from typing import Annotated

from fastapi import Depends, Request

from .core.annotation import AnnotationQueue


def get_db(request: Request) -> dict:
    """Return the database instance stored in the application state."""
    return request.app.state.database()


DatabaseDepends = Annotated[dict, Depends(get_db)]

# Queue that processess annotation tasks safely between threads
annotation_queue = AnnotationQueue()
