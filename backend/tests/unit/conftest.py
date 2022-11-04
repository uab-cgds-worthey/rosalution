"""Fixture configuration used for all unit tests"""
import queue
from unittest.mock import Mock
import pytest

from src.core.annotation import AnnotationService
from src.models.analysis import Analysis
from src.repository.analysis_collection import AnalysisCollection
from src.repository.annotation_config_collection import AnnotationConfigCollection
from src.repository.genomic_unit_collection import GenomicUnitCollection
from src.repository.gridfs_bucket_collection import GridFSBucketCollection

from ..test_utils import read_database_fixture, read_test_fixture, mock_mongo_collection


@pytest.fixture(name="analysis_collection_json")
def fixture_analysis_collection_json():
    """Returns the JSON for the analyses collection used to seed the MongoDB database"""
    return read_database_fixture("analyses.json")


@pytest.fixture(name="updated_analysis_collection_json")
def fixture_updated_analysis_collection_json():
    """Returns the JSON for the analyses collection used to seed the MongoDB database"""
    return read_test_fixture("analysis-update.json")


@pytest.fixture(name="analysis_collection")
def fixture_analysis_collection(analysis_collection_json, updated_analysis_collection_json):
    """Returns the analysis collection to be mocked"""
    mock_collection = mock_mongo_collection()
    mock_collection.find = Mock(return_value=analysis_collection_json)
    mock_collection.find_one = Mock(return_value=analysis_collection_json)
    mock_collection.find_one_and_update = Mock(return_value=updated_analysis_collection_json)
    return AnalysisCollection(mock_collection)


@pytest.fixture(name="gridfs_bucket_collection")
def fixture_gridfs_bucket_collection():
    """Returns the GridFS bucket collection to be mocked"""
    mock_bucket = Mock()
    mock_collection = GridFSBucketCollection(mock_bucket)
    mock_collection.bucket.exists = Mock(return_value=True)
    mock_collection.bucket.put = Mock(return_value="633afb87fb250a6ea1569555")
    mock_collection.bucket.list = Mock(return_value=["test.txt"])
    mock_collection.bucket.get = Mock(return_value="test.txt")
    mock_collection.bucket.delete = Mock(return_value=None)
    return mock_collection


@pytest.fixture(name="genomic_unit_collection_json")
def fixture_genomic_unit_collection_json():
    """Returns the JSON for the genomic units collection used to seed the MongoDB database"""
    return read_database_fixture("genomic-units.json")


@pytest.fixture(name="genomic_unit_collection")
def fixture_genomic_unit_collection(genomic_unit_collection_json):
    """Returns a genomic unit collection"""

    mock_collection = mock_mongo_collection()
    mock_collection.find = Mock(return_value=genomic_unit_collection_json)

    return GenomicUnitCollection(mock_collection)


@pytest.fixture(name="cpam0002_analysis_json")
def fixture_cpam0002_analysis_json(analysis_collection_json):
    """JSON for the CPAM0002 Analysis"""
    return next((analysis for analysis in analysis_collection_json if analysis['name'] == "CPAM0002"), None)


@pytest.fixture(name="cpam0002_analysis")
def fixture_analysis(cpam0002_analysis_json):
    """Fixture for the CPAM0002 Analysis"""
    return Analysis(**cpam0002_analysis_json)


@pytest.fixture(name="cpam0046_analysis")
def fixture_cpam0046_analysis(analysis_collection_json):
    """Returns the Analysis for CPAM0046 to verify creating annotation tasks"""
    analysis_json = next((analysis for analysis in analysis_collection_json if analysis['name'] == "CPAM0046"), None)
    return Analysis(**analysis_json)


@pytest.fixture(name="annotation_collection")
def fixture_annotation_collection():
    """Returns the annotation collection for the datasets to be mocked"""
    mock_collection = mock_mongo_collection()
    mock_collection.find = Mock(return_value=read_database_fixture("annotations-config.json"))
    mock_collection.find_one = Mock(return_value=read_database_fixture("annotations-config.json"))
    return AnnotationConfigCollection(mock_collection)


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
    """ Annotation queue using the CPAM0002 analysis fixtures """
    annotation_service = AnnotationService(annotation_collection)
    test_queue = queue.Queue()
    annotation_service.queue_annotation_tasks(cpam0002_analysis, test_queue)
    return test_queue


@pytest.fixture(name="transcript_annotation_response")
def fixture_annotation_response_for_transcript():
    """Returns a mocked response from a web page, particularly ensembl"""
    return [{
        "transcript_consequences": [{
            "sift_prediction": "deleterious",
            "gene_symbol": "VMA21",
            "transcript_id": "NM_001017980.4",
            "polyphen_score": 0.597,
            "polyphen_prediction": "possibly_damaging",
            "sift_score": 0.02,
            "cds_start": 164,
            "variant_allele": "T",
            "used_ref": "G",
            "consequence_terms": ["missense_variant", "splice_region_variant"],
        }, {
            "transcript_id": "NM_001363810.1",
            "sift_score": 0.01,
            "gene_symbol": "VMA21",
            "polyphen_prediction": "probably_damaging",
            "sift_prediction": "deleterious",
            "polyphen_score": 0.998,
            "used_ref": "G",
            "cds_start": 329,
            "variant_allele": "T",
            "consequence_terms": ["missense_variant", "splice_region_variant"],
        }]
    }]


@pytest.fixture(name="empty_pedigree")
def fixture_empty_pedigree():
    """returns an analysis with an empty pedigree"""
    return read_test_fixture("empty-pedigree.json")
