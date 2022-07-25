"""Module user09es interface to the repository in the data layer that stores the persistent state of the application"""
# pylint: disable=too-few-public-methods
# This wrapper is intended to create a callable instance for FastAPI Depedency Injection
# there is no need to include any additional methods
from .repository.user_collection import UserCollection
from .repository.analysis_collection import AnalysisCollection
from .repository.annotation_collection import AnnotationCollection
from .repository.genomic_unit_collection import GenomicUnitCollection

class Database:
    """Interface for collections and additional resources for user09ing persistent state of the application"""

    def __init__(self, client):
        """Accepts a configured MongoDB database client.  Does not connect until first operation is user09ed"""
        self.database_client = client

        # "An important note about collections (and databases) in MongoDB is that
        # they are created lazily - none of the above commands have actually
        # performed any operations on the MongoDB server. Collections and
        # databases are created when the first document is inserted into them.
        # This is why it is safe to include these operations within
        # a constructuro since there is not chance for failure creating/
        # allocating the object."
        # https://pymongo.readthedocs.io/en/stable/tutorial.html#getting-a-collection

        # self.collections = {
        #   'analysis': AnalysisCollection(self.database_client.db['analysis']),
        #   'annotation': AnnotationCollection(self.database_client.db['annotation'])
        # }

        self.collections = {
            "analysis": AnalysisCollection(),
            "annotation": AnnotationCollection(),
            "genomic_unit": GenomicUnitCollection(),
            "user": UserCollection()
        }

    def __call__(self):
        """
        Returns the injected dependency instance to use for sharing the repository collections to routes
        See FastAPI docs to learn more https://fastapi.tiangolo.com/advanced/advanced-dependencies/#a-callable-instance
        """
        return self.collections
