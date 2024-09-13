"""Fixture configuration used for all unit tests"""
import queue
from unittest.mock import Mock
import pytest

from src.core.annotation_unit import AnnotationUnit
from src.config import Settings
from src.core.annotation import AnnotationService
from src.models.analysis import Analysis
from src.repository.analysis_collection import AnalysisCollection
from src.repository.annotation_config_collection import AnnotationConfigCollection
from src.repository.genomic_unit_collection import GenomicUnitCollection
from src.repository.gridfs_bucket_collection import GridFSBucketCollection

from ..test_utils import read_test_fixture, mock_mongo_collection


@pytest.fixture(name="cpam0002_analysis_json")
def fixture_cpam0002_analysis_json():
    """JSON for the CPAM0002 Analysis"""
    return read_test_fixture("analysis-CPAM0002.json")


@pytest.fixture(name="cpam0046_analysis_json")
def fixture_cpam0046_analysis_json():
    """JSON for the CPAM0046 Analysis"""
    return read_test_fixture("analysis-CPAM0046.json")


@pytest.fixture(name="cpam0112_analysis_json")
def fixture_cpam0112_analysis_json():
    """JSON for the CPAM0112 Analysis"""
    return read_test_fixture("analysis-CPAM0112.json")


@pytest.fixture(name="cpam0002_analysis")
def fixture_analysis(cpam0002_analysis_json):
    """Fixture for the CPAM0002 Analysis"""
    return Analysis(**cpam0002_analysis_json)


@pytest.fixture(name="cpam0046_analysis")
def fixture_cpam0046_analysis(cpam0046_analysis_json):
    """Returns the Analysis for CPAM0046 to verify creating annotation tasks"""
    return Analysis(**cpam0046_analysis_json)


@pytest.fixture(name="analysis_collection_json")
def fixture_analysis_collection_json(cpam0002_analysis_json, cpam0046_analysis_json, cpam0112_analysis_json):
    """Returns the multiple analyses being mocked as an array"""
    return [cpam0002_analysis_json, cpam0046_analysis_json, cpam0112_analysis_json]


@pytest.fixture(name="analysis_collection")
def fixture_analysis_collection(analysis_collection_json):
    """Returns the analysis collection to be mocked"""
    mock_collection = mock_mongo_collection()
    mock_collection.find = Mock(return_value=analysis_collection_json)
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


@pytest.fixture(name="gene_vma21_annotations_json")
def fixture_gene_annotation_json():
    """JSON for the annotations of the Gene VMA21"""
    return read_test_fixture("annotations-VMA21.json")


@pytest.fixture(name="variant_nm001017980_3_c_164g_t_annotations_json")
def fixture_hgvs_variant_json():
    """JSON for the annotations of the Gene VMA21"""
    return read_test_fixture("annotations-NM001017980_3_c_164G_T.json")


@pytest.fixture(name="genomic_unit_collection_json")
def fixture_genomic_unit_collection_json(gene_vma21_annotations_json, variant_nm001017980_3_c_164g_t_annotations_json):
    """Returns array of JSON for the genomic units within the collection"""
    return [gene_vma21_annotations_json, variant_nm001017980_3_c_164g_t_annotations_json]


@pytest.fixture(name="genomic_unit_collection")
def fixture_genomic_unit_collection(genomic_unit_collection_json):
    """Returns a genomic unit collection"""

    mock_collection = mock_mongo_collection()
    mock_collection.find = Mock(return_value=genomic_unit_collection_json)

    return GenomicUnitCollection(mock_collection)


@pytest.fixture(name="annotation_config_collection_json")
def fixture_annotation_config_collection_json():
    """Returns the json for the annotation configuration"""

    return read_test_fixture("annotations-config.json")


@pytest.fixture(name="annotation_config_collection")
def fixture_annotation_config_collection(annotation_config_collection_json):
    """Returns the annotation collection for the datasets to be mocked"""
    mock_collection = mock_mongo_collection()
    mock_collection.find = Mock(return_value=annotation_config_collection_json)
    mock_collection.find_one = Mock(return_value=read_test_fixture("annotations-config.json"))
    return AnnotationConfigCollection(mock_collection)


@pytest.fixture(name='get_dataset_manifest_config')
def get_dataset_manifest_config(analysis_collection_json):
    """Fixture factory method to create an dataset from the genomic unit information and name of the datset."""

    def _create_dataset_manifest(analysis_name, dataset_name):
        """Method to create the dataset manifest config"""

        analysis_json = next((item for item in analysis_collection_json if item['name'] == analysis_name), None)
        analysis = Analysis(**analysis_json)
        dataset_manifest = next((item for item in analysis.manifest if dataset_name in item), None)

        dataset_config = {
            "data_set": dataset_name, "data_source": dataset_manifest[dataset_name]['data_source'],
            "version": dataset_manifest[dataset_name]['version']
        }

        return dataset_config

    return _create_dataset_manifest



@pytest.fixture(name="cpam0046_analysis")
def fixture_cpam0046_analysis(cpam0046_analysis_json):
    """Returns the Analysis for CPAM0046 to verify creating annotation tasks"""
    return Analysis(**cpam0046_analysis_json)


@pytest.fixture(name="genomic_units_with_types")
def fixture_genomic_units_with_types(analysis_collection_json):
    """Returns the multiple analyses being mocked as an array"""

    def get_units(analysis_json):
        analysis = Analysis(**analysis_json)
        return analysis.units_to_annotate()

    genomic_units_lists = list(map(get_units, analysis_collection_json))
    flattened_list = [unit for analysis_units in genomic_units_lists for unit in analysis_units]
    types = {unit['unit']: unit['type'] for unit in flattened_list}
    return types


@pytest.fixture(name='get_annotation_unit')
def get_standard_annotation_unit(annotation_config_collection_json, genomic_units_with_types):
    """Fixture factory method to create an AnnotationUnit from the genomic unit information and name of the datset."""

    # units = {
    #     'VMA21': GenomicUnitType.GENE,
    #     'NM_001017980.3:c.164G>T': GenomicUnitType.HGVS_VARIANT
    # }

    def _create_annotation_unit(genomic_unit_name, dataset_name):
        """Method to create the Annotation Unit"""
        genomic_unit_type = genomic_units_with_types[genomic_unit_name]
        genomic_unit = {'unit': genomic_unit_name, 'type': genomic_unit_type}
        dataset_config = next((unit for unit in annotation_config_collection_json if unit['data_set'] == dataset_name),
                              None)

        return AnnotationUnit(genomic_unit, dataset_config)

    return _create_annotation_unit


@pytest.fixture(name='get_annotation_json')
def get_annotation_json(genomic_unit_collection_json):
    """Fixture factory method to create an return the JSON from the genomic unit """

    def _get_annotation_json(genomic_unit_name, genomic_unit_type):
        """ Provides a genomic unit from the genomic unit collection, otherwise returns false"""

        unit_type = genomic_unit_type.value
        return next((
            unit for unit in genomic_unit_collection_json if unit_type in unit and unit[unit_type] == genomic_unit_name
        ), None)

    return _get_annotation_json


@pytest.fixture(name="cpam0046_annotation_queue")
def fixture_cpam0046_annotation_queue(annotation_config_collection, cpam0046_analysis):
    """
    Returns an thread-safe annotation queue with tasks
    """
    annotation_service = AnnotationService(annotation_config_collection)
    test_queue = queue.Queue()
    annotation_service.queue_annotation_tasks(cpam0046_analysis, test_queue)
    return test_queue


@pytest.fixture(name="cpam0002_annotation_queue")
def fixture_cpam0002_annotation_queue(annotation_config_collection, cpam0002_analysis):
    """ Annotation queue using the CPAM0002 analysis fixtures """
    annotation_service = AnnotationService(annotation_config_collection)
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


@pytest.fixture(name="settings_json")
def fixture_settings_json():
    """Returns the settings for a fake rosalution. Mostly used for security functionality/testing"""
    return read_test_fixture("application_settings.json")


@pytest.fixture(name="settings")
def fixture_rosalution_settings(settings_json):
    """Returns an instance of the settings with the mocked JSON that is unpacked"""
    return Settings(**settings_json)


@pytest.fixture(name="users_json")
def fixture_users_json():
    """Returns the JSON for the users collection used to seed the MongoDB database"""
    return read_test_fixture("users-test-fixture.json")
