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

@pytest.fixture(name="cpam0046_annotation_queue")
def fixture_cpam0046_annotation_queue(annotation_collection, cpam0046_analysis):
    """
    Returns an thread-safe annotation queue with tasks
    """
    annotation_service = AnnotationService(annotation_collection)
    test_queue = queue.Queue()
    annotation_service.queue_annotation_tasks(cpam0046_analysis, test_queue)
    return test_queue

@pytest.fixture(name="cpam0002_annotation_queue")
def fixture_cpam0002_annotation_queue(annotation_collection, cpam0002_analysis):
    annotation_service = AnnotationService(annotation_collection)
    test_queue = queue.Queue()
    annotation_service.queue_annotation_tasks(cpam0002_analysis, test_queue)
    return test_queue

@pytest.fixture(name="transcript_annotation_response")
def fixture_annotation_response_for_transcript():
    """ Returns a mocked response from a web page, particularly ensembl  """
    return {
        "transcript_consequences": [
            {
                "sift_prediction": "deleterious",
                "gene_symbol": "VMA21",
                "transcript_id": "NM_001017980.4",
                "polyphen_score": 0.597,
                "polyphen_prediction": "possibly_damaging",
                "sift_score": 0.02,
                "cds_start":164,
                "variant_allele":"T",
                "used_ref":"G",
                "consequence_terms":[
                    "missense_variant",
                    "splice_region_variant"
                ],
            },
            {
                "transcript_id": "NM_001363810.1",
                "sift_score": 0.01,
                "gene_symbol": "VMA21",
                "polyphen_prediction": "probably_damaging",
                "sift_prediction": "deleterious",
                "polyphen_score": 0.998,
                "used_ref":"G",
                "cds_start":329,
                "variant_allele":"T",
                "consequence_terms":[
                    "missense_variant",
                    "splice_region_variant"
                ],
            }
        ]
    }
