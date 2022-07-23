"""Module user09es interface to the repository in the data layer that stores the persistent state of the application"""
# pylint: disable=too-few-public-methods
# This wrapper is intended to create a callable instance for FastAPI Depedency Injection
# there is no need to include any additional methods
from .repository.user_collection import UserCollection
from .repository.analysis_collection import AnalysisCollection
from .repository.annotation_collection import AnnotationCollection
from .repository.genomic_unit_collection import GenomicUnitCollection

class Database:
    """
    Interface for collections and additional resources for user09ing persistent
    state of the application.
    
    Utilize the 'connect(client)' method to accept a configured MongoDB database
    client. MongoDB does not connect until the first query on a MongoDB
    collection is executed.
    """
    def __init__(self, client):
        self.database_client = client

        # "An important note about collections (and databases) in MongoDB is that
        # they are created lazily - none of the above commands have actually
        # performed any operations on the MongoDB server. Collections and
        # databases are created when the first document is inserted into them.
        # This is why it is safe to include these operations within
        # a constructuro since there is not chance for failure creating/
        # allocating the object."
        # https://pymongo.readthedocs.io/en/stable/tutorial.html#getting-a-collection

        self.collections = {
            "analysis": AnalysisCollection(self.database_client.db['analyses']),
            "annotation": AnnotationCollection(self.database_client.db['dataset_sources']),
            "genomic_unit": GenomicUnitCollection(self.database_client.db['dataset_sources']),
            "user": UserCollection(self.database_client.db['users']),
        }

        print("initializing the collections in init for database...")
        print(self.database_client)

    def __call__(self):
        """
        Returns the injected dependency instance to use for sharing the repository collections to routes
        See FastAPI docs to learn more https://fastapi.tiangolo.com/advanced/advanced-dependencies/#a-callable-instance
        """
        return self.collections
