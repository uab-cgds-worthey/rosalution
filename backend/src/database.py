"""Module manages interface to the repository in the data layer that stores the persistent state of the application"""
# pylint: disable=too-few-public-methods
# This wrapper is intended to create a callable instance for FastAPI Depedency Injection
# there is no need to include any additional methods
from .repository.gridfs_bucket_collection import GridFSBucketCollection
from .repository.user_collection import UserCollection
from .repository.analysis_collection import AnalysisCollection
from .repository.annotation_config_collection import AnnotationConfigCollection
from .repository.genomic_unit_collection import GenomicUnitCollection
from .repository.project_repository import ProjectRepository


class Database:
    """
    Interface for collections and additional resources for persistent
    state of the application.

    Utilize the 'connect(client)' method to accept a configured MongoDB database
    client. MongoDB does not connect until the first query on a MongoDB
    collection is executed.
    """

    def __init__(self, client, gridfs_bucket):
        self.database_client = client

        # "An important note about collections (and databases) in MongoDB is that
        # they are created lazily - none of the above commands have actually
        # performed any operations on the MongoDB server. Collections and
        # databases are created when the first document is inserted into them.
        # This is why it is safe to include these operations within
        # a constructuro since there is not chance for failure creating/
        # allocating the object."
        # https://pymongo.readthedocs.io/en/stable/tutorial.html#getting-a-collection
        self.database = self.database_client.rosalution_db
        self.collections = {
            "analysis": AnalysisCollection(self.database['analyses']),
            "annotation_config": AnnotationConfigCollection(self.database['annotations_config']),
            "genomic_unit": GenomicUnitCollection(self.database['genomic_units']),
            "user": UserCollection(self.database['users']),
            "project": ProjectRepository(self.database['users'], self.database['analyses']),
            "bucket": GridFSBucketCollection(gridfs_bucket),
        }

    def __call__(self):
        """
        Returns the injected dependency instance to use for sharing the repository collections to routes
        See FastAPI docs to learn more https://fastapi.tiangolo.com/advanced/advanced-dependencies/#a-callable-instance
        """
        return self.collections
