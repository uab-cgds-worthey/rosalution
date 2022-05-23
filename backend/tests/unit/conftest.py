"""Fixture configuration used for all unit tests"""
import queue
import pytest

from src.repository.analysis_collection import AnalysisCollection
from src.repository.annotation_collection import AnnotationCollection
from src.annotation import AnnotationService


@pytest.fixture(name="analysis_collection")
def fixture_analysis_collection():
    """Returns the analysis collection to be mocked"""
    return AnalysisCollection()

@pytest.fixture(name="annotation_collection")
def fixture_annotation_collection():
    """
    Returns the annotation collection for the configuration to verify
    annotation tasks are created according to the configuration
    """
    # mock_collection = Mock()
    # mock_collection.find = Mock( return_value = read_fixture("annotation-sources.json") )
    # return AnnotationCollection(mock_collection)
    return AnnotationCollection()

# @pytest.fixture(name="database_collection")
# def fixture_analysis_database_collection():
#     """Provides a mock for the database client"""
#     mock_database_collection = Mock()
#     return mock_database_collection

@pytest.fixture(name="annotation_queue")
def fixture_annotation_queue(annotation_collection, cpam0046_analysis):
    """
    Returns an thread-safe annotation queue with tasks
    """
    annotation_service = AnnotationService(annotation_collection)
    test_queue = queue.Queue()
    annotation_service.queue_annotation_tasks(cpam0046_analysis, test_queue)
    return test_queue
