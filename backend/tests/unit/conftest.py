"""Fixture configuration used for all unit tests"""
import queue
from unittest.mock import AsyncMock, MagicMock, Mock
import pytest

from src.core.annotation_task import HttpAnnotationTask, VersionAnnotationTask
from src.core.annotation_unit import AnnotationUnit
from src.config import Settings
from src.core.annotation import AnnotationService
from src.enums import GenomicUnitType
from src.models.analysis import Analysis
from src.repository.analysis_collection import AnalysisCollection
from src.repository.annotation_config_collection import AnnotationConfigCollection
from src.repository.genomic_unit_collection import GenomicUnitCollection
from src.repository.gridfs_bucket_collection import GridFSBucketCollection
from src.repository.user_collection import UserCollection

from ..test_utils import read_test_fixture, mock_mongo_collection


@pytest.fixture(name="cpam0002_analysis_json")
def fixture_cpam0002_analysis_json():
    """JSON for the CPAM0002 Analysis"""
    return read_test_fixture("analysis-CPAM0002.unit.json")


@pytest.fixture(name="cpam0046_analysis_json")
def fixture_cpam0046_analysis_json():
    """JSON for the CPAM0046 Analysis"""
    return read_test_fixture("analysis-CPAM0046.unit.json")


@pytest.fixture(name="cpam0112_analysis_json")
def fixture_cpam0112_analysis_json():
    """JSON for the CPAM0112 Analysis"""
    return read_test_fixture("analysis-CPAM0112.unit.json")


@pytest.fixture(name="cpam0002_analysis")
def fixture_analysis(cpam0002_analysis_json):
    """Fixture for the CPAM0002 Analysis"""
    return Analysis(**cpam0002_analysis_json)


@pytest.fixture(name="cpam0046_analysis")
def fixture_cpam0046_analysis(cpam0046_analysis_json):
    """Returns the Analysis for CPAM0046 to verify creating annotation tasks"""
    return Analysis(**cpam0046_analysis_json)


@pytest.fixture(name="cpam0112_analysis")
def fixture_cpam0112_analysis(cpam0112_analysis_json):
    """Returns the Analysis for CPAM0112 to verify creating annotation tasks that has forge with cached dependency"""
    return Analysis(**cpam0112_analysis_json)


@pytest.fixture(name="analysis_collection_json")
def fixture_analysis_collection_json(cpam0002_analysis_json, cpam0046_analysis_json, cpam0112_analysis_json):
    """Returns the multiple analyses being mocked as an array"""
    return [cpam0002_analysis_json, cpam0046_analysis_json, cpam0112_analysis_json]


@pytest.fixture(name="analysis_collection")
def fixture_analysis_collection(analysis_collection_json):
    """Returns the analysis collection to be mocked"""
    mock_collection = mock_mongo_collection()
    mock_cursor = MagicMock()
    mock_cursor.to_list = AsyncMock(return_value=analysis_collection_json)
    mock_collection.find = MagicMock(return_value=mock_cursor)
    return AnalysisCollection(mock_collection)


@pytest.fixture(name="gridfs_bucket_collection")
def fixture_gridfs_bucket_collection():
    """Returns the GridFS bucket collection to be mocked"""
    mock_bucket = Mock()
    mock_collection = GridFSBucketCollection(mock_bucket)
    mock_collection.bucket.exists = AsyncMock(return_value=True)
    mock_collection.bucket.put = AsyncMock(return_value="633afb87fb250a6ea1569555")
    mock_collection.bucket.list = AsyncMock(return_value=["test.txt"])
    mock_collection.bucket.get = AsyncMock(return_value="test.txt")
    mock_collection.bucket.delete = AsyncMock(return_value=None)
    return mock_collection


@pytest.fixture(name="gene_vma21_annotations_json")
def fixture_gene_annotation_json():
    """JSON for the annotations of the Gene VMA21"""
    return read_test_fixture("annotations-VMA21.unit.json")


@pytest.fixture(name="variant_nm001017980_3_c_164g_t_annotations_json")
def fixture_hgvs_variant_json():
    """JSON for the annotations of the Gene VMA21"""
    return read_test_fixture("annotations-NM001017980_3_c_164G_T.unit.json")


@pytest.fixture(name="genomic_unit_collection_json")
def fixture_genomic_unit_collection_json(gene_vma21_annotations_json, variant_nm001017980_3_c_164g_t_annotations_json):
    """Returns array of JSON for the genomic units within the collection"""
    return [gene_vma21_annotations_json, variant_nm001017980_3_c_164g_t_annotations_json]


@pytest.fixture(name="genomic_unit_collection")
def annotation_config_collectionfixture_genomic_unit_collection(genomic_unit_collection_json):
    """Returns a genomic unit collection"""

    mock_collection = mock_mongo_collection()
    mock_cursor = MagicMock()
    mock_cursor.to_list = AsyncMock(return_value=genomic_unit_collection_json)
    mock_collection.find = MagicMock(return_value=mock_cursor)

    return GenomicUnitCollection(mock_collection)


@pytest.fixture(name="annotation_config_collection_json")
def fixture_annotation_config_collection_json():
    """Returns the json for the annotation configuration"""

    return read_test_fixture("annotations-config.unit.json")


@pytest.fixture(name="annotation_config_collection")
def fixture_annotation_config_collection(annotation_config_collection_json):
    """Returns the annotation collection for the datasets to be mocked"""
    mock_collection = mock_mongo_collection()
    mock_cursor = MagicMock()
    mock_cursor.to_list = AsyncMock(return_value=annotation_config_collection_json)
    mock_collection.find = MagicMock(return_value=mock_cursor)
    mock_collection.find_one = Mock(return_value=read_test_fixture("annotations-config.unit.json"))
    return AnnotationConfigCollection(mock_collection)


@pytest.fixture(name="annotation_config_collection_with_forge_using_cached_dataset")
def fixture_annotation_config_collection_with_cached_dataset():
    """Returns the annotation collection for the datasets to be mocked"""

    json_from_fixture = read_test_fixture("annotations-config-with-forge-using-cached-dependnecy.json")
    mock_collection = mock_mongo_collection()
    mock_collection.find = Mock(return_value=json_from_fixture)
    mock_collection.find_one = Mock(return_value=read_test_fixture("annotations-config.json"))
    return AnnotationConfigCollection(mock_collection)


@pytest.fixture(name='get_dataset_manifest_config')
def fixture_get_dataset_manifest_config(analysis_collection_json):
    """Fixture factory method to create an dataset from the genomic unit information and name of the datset."""

    def _create_dataset_manifest(analysis_name, omic_unit, dataset_name):
        """Method to create the dataset manifest config"""

        analysis_json = next((item for item in analysis_collection_json if item['name'] == analysis_name), None)
        analysis = Analysis(**analysis_json)

        omic_unit_manifest = next(
            (omic_manifest for omic_manifest in analysis.manifest if omic_manifest['unit'] == omic_unit), None
        )
        # print(omic_unit_manifest)
        # print(dataset_name)
        dataset_manifest = next((item for item in omic_unit_manifest['manifest'] if dataset_name in item), None)
        # print(dataset_manifest)
        # print('why None but its printing?', dataset_manifest)
        # print(dataset_manifest[dataset_name])
        # print(dataset_manifest[dataset_name]['data_source'])
        dataset_config = {
            "data_set": dataset_name, "data_source": dataset_manifest[dataset_name]['data_source'],
            "version": dataset_manifest[dataset_name]['version']
        }
        return dataset_config

    return _create_dataset_manifest


@pytest.fixture(name="genomic_units_with_types")
def fixture_genomic_units_with_types(analysis_collection_json):
    """Returns the multiple analyses being mocked as an array"""

    def get_units(analysis_json):
        analysis = Analysis(**analysis_json)
        return analysis.get_all_units_to_annotate()

    genomic_units_lists = list(map(get_units, analysis_collection_json))
    flattened_list = [unit for analysis_units in genomic_units_lists for unit in analysis_units]
    types = {unit['unit']: unit['type'] for unit in flattened_list}
    return types


@pytest.fixture(name='get_annotation_unit')
def get_standard_annotation_unit(annotation_config_collection_json, genomic_units_with_types):
    """
    Fixture factory method to create an AnnotationUnit from the available genomic units in the analyses from
    'analysis_collection_json' fixture. It searches the 'annotation_config_collection_json' to pair with
    the genomic unit to create an AnnotationUnit.

    {
      'VMA21': GenomicUnitType.GENE,
      'NM_001017980.3:c.164G>T': GenomicUnitType.HGVS_VARIANT
    }
    """

    def _create_annotation_unit(genomic_unit_name, dataset_name):
        """Method to create the Annotation Unit"""
        genomic_unit_type = genomic_units_with_types[genomic_unit_name]
        genomic_unit = {'unit': genomic_unit_name, 'type': genomic_unit_type}
        dataset_config = next((unit for unit in annotation_config_collection_json if unit['data_set'] == dataset_name),
                              None)

        return AnnotationUnit(genomic_unit, dataset_config)

    return _create_annotation_unit


@pytest.fixture(name="get_version_task")
def get_version_annotation_task(get_annotation_unit):
    """creating version task"""

    def _create_version_task(genomic_unit, dataset_name):

        annotation_unit = get_annotation_unit(genomic_unit, dataset_name)

        return VersionAnnotationTask(annotation_unit)

    return _create_version_task


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
async def fixture_cpam0046_annotation_queue(annotation_config_collection, cpam0046_analysis):
    """
    Returns an thread-safe annotation queue with tasks
    """
    annotation_service = AnnotationService(annotation_config_collection)
    test_queue = queue.Queue()
    await annotation_service.queue_annotation_tasks(cpam0046_analysis, test_queue)
    return test_queue


@pytest.fixture(name="cpam0002_annotation_queue")
async def fixture_cpam0002_annotation_queue(annotation_config_collection, cpam0002_analysis):
    """ Annotation queue using the CPAM0002 analysis fixtures """
    annotation_service = AnnotationService(annotation_config_collection)
    test_queue = queue.Queue()
    await annotation_service.queue_annotation_tasks(cpam0002_analysis, test_queue)
    return test_queue


@pytest.fixture(name="cpam0112_annotation_queue")
def fixture_cpam0112_annotation_queue(annotation_config_collection_with_forge_using_cached_dataset, cpam0112_analysis):
    """
    Returns an thread-safe annotation queue with tasks
    """
    annotation_service = AnnotationService(annotation_config_collection_with_forge_using_cached_dataset)
    test_queue = queue.Queue()
    annotation_service.queue_annotation_tasks(cpam0112_analysis, test_queue)
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
    return read_test_fixture("application_settings.shared.json")


@pytest.fixture(name="settings")
def fixture_rosalution_settings(settings_json):
    """Returns an instance of the settings with the mocked JSON that is unpacked"""
    return Settings(**settings_json)


@pytest.fixture(name="users_json")
def fixture_users_json():
    """Returns the JSON for the users collection used to seed the MongoDB database"""
    return read_test_fixture("users-test-fixture.unit.json")


@pytest.fixture(name="user_collection")
def fixture_users_collection(users_json):
    """Returns the annotation collection for the datasets to be mocked"""
    mock_collection = mock_mongo_collection()
    mock_collection.find_one = AsyncMock(return_value=users_json[0])
    return UserCollection(mock_collection)


@pytest.fixture(name="hgvs_variant_genomic_unit_for_annotation_tasks")
def fixture_genomic_unit():
    """Returns the genomic unit 'NM_170707.3:c.745C>T' to be annotated"""
    return {
        "unit": "NM_170707.3:c.745C>T",
        "genomic_unit_type": GenomicUnitType.HGVS_VARIANT,
        "transcript": "NM_170707",
    }


@pytest.fixture(name="gene_hpo_dataset")
def fixture_gene_hpo_dataset():
    """
    Returns the dict of the HPO dataset that has a dependency
    """
    return {
        "data_set": "HPO", "data_source": "HPO", "genomic_unit_type": "gene", "annotation_source_type": "http",
        "url": "https://hpo.jax.org/api/hpo/gene/{Entrez Gene Id}", "dependencies": ["Entrez Gene Id"],
        "attribute": "{ \"diseaseAssoc\": [.diseaseAssoc[].diseaseName]}", "versioning_type": "date"
    }


@pytest.fixture(name="gene_genomic_unit")
def fixture_gene_genomic_unit():
    """Returns the genomic unit 'VMA21' to be annotated"""
    return {
        "unit": "VMA21",
        "Entrez Gene Id": "45614",
        # "genomic_unit_type": GenomicUnitType.GENE,
        "type": GenomicUnitType.GENE
    }


@pytest.fixture(name="gene_hpo_annotation_unit")
def fixture_gene_annotation__unit(gene_genomic_unit, gene_hpo_dataset):
    """Returns the genomic unit 'VMA21' to be annotated"""
    return AnnotationUnit(gene_genomic_unit, gene_hpo_dataset)


@pytest.fixture(name="http_annotation_task_gene")
def fixture_http_annotation_empty(gene_hpo_annotation_unit):
    """Returns an HTTP annotation taskd"""
    task = HttpAnnotationTask(gene_hpo_annotation_unit)
    return task


@pytest.fixture(name="hpo_annotation_response")
def fixture_hpo_annotation_response():
    """
    Returns an object that contains the actual return aoutput for GENE VMA21 for HPO terms
    """
    return {
        "gene": {"entrezGeneId": 203547, "entrezGeneSymbol": "VMA21"},
        "termAssoc": [
            {"ontologyId": "HP:0001270", "name": "Motor delay", "definition": "A type of Developmental delay crized"},
            {"ontologyId": "HP:0001419", "name": "X-linked recessive inheritance", "definition": "A mode of inheriee."},
            {"ontologyId": "HP:0001371", "name": "Flexion contracture", "definition": "A flexion contracnt of joints."},
            {"ontologyId": "HP:0003391", "name": "Gowers sign", "definition": "A phenomenon whereby patie"},
            {"ontologyId": "HP:0008994", "name": "Proximal muscle weakness in lower limbs", "definition": "lack legs."},
            {"ontologyId": "HP:0002650", "name": "Scoliosis", "definition": "The presence of an abnormal lateral curv"},
            {"ontologyId": "HP:0003551", "name": "Difficulty climbing stairs", "definition": "Reduced abilit climb."},
            {"ontologyId": "HP:0002093", "name": "Respiratory insufficiency", "definition": ""},
            {"ontologyId": "HP:0003198", "name": "Myopathy", "definition": "A disorder of to impairment"},
            {"ontologyId": "HP:0009046", "name": "Difficulty running", "definition": "Reduced ability to run."},
            {"ontologyId": "HP:0003202", "name": "Skeletal muscle atrophy", "definition": "The presence of skeletal "},
            {"ontologyId": "HP:0001319", "name": "Neonatal hypotonia", "definition": "Muscular hypotonia (abnormally "},
            {
                "ontologyId": "HP:0003236", "name": "Elevated circulating creatine kinase concentration",
                "definition": "A"
            },
            {"ontologyId": "HP:0002486", "name": "Myotonia", "definition": "An involuntartrical stimulation."},
            {"ontologyId": "HP:0007941", "name": "Limited extraocular movements", "definition": "Limitehe"},
        ],
        "diseaseAssoc": [{
            "diseaseId": "OMIM:310440", "diseaseName": "Myopathy, X-linked, With Excessive Autophagy", "dbId": "310440",
            "db": "OMIM"
        }],
    }
