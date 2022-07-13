"""Tests Annotation Tasks and the creation of them"""
import pytest
from src.enums import GenomicUnitType
from src.annotation_task import AnnotationTaskFactory, HttpAnnotationTask, recurse

def test_http_annotation_base_url(http_annotation_transcript_id):
    """Verifies if the HTTP annotation creates the base url using the url and genomic_unit as expected."""
    actual = http_annotation_transcript_id.base_url()
    assert actual == "http://grch37.rest.ensembl.org/vep/human/hgvs/NM_170707.3:c.745C>T?content-type=application/json;"

def test_http_annotation_identifier(http_annotation_transcript_id):
    """Verifies that the HTTP annotation creates the identifier as expected"""
    actual = http_annotation_transcript_id.identifier()
    assert actual == "http://grch37.rest.ensembl.org/vep/human/hgvs/NM_170707.3:c.745C>T?content-type=application/json;"

# def test_annotation_task_base_url_if_not_datasets(annotation_task):
#     Keeping this as a placeholder in case this gets added back in
#     """Verifies that an annotation task can return what the base url is for a genomic unit"""
#     assert annotation_task.base_url() is None

def test_http_annotation_task_base_url_many_datasets(
    http_annotation_task_many_datasets,
):
    """Verifies that the HTTP annotation task creates the base url using the 'url' and the genomic unit"""
    actual = http_annotation_task_many_datasets.base_url()
    assert actual == "http://grch37.rest.ensembl.org/vep/human/hgvs/NM_170707.3:c.745C>T?content-type=application/json;"

def test_http_annotation_task_build_url(http_annotation_task_many_datasets):
    """Verifies that the HTTP annotation task builds the complete URL including the base url and the query params"""
    actual = http_annotation_task_many_datasets.build_url()
    expected = (
        "http://grch37.rest.ensembl.org/vep/human/hgvs/NM_170707.3:c.745C>T?content-type=application/json;refseq=1;"
    )
    assert actual == expected

def test_annotation_task_create_http_task(hgvs_variant_genomic_unit, transcript_id_dataset):
    """Verifies that the annotation task factory creates the correct annotation task according to the dataset type"""
    actual_identifier, actual_task = AnnotationTaskFactory.create(hgvs_variant_genomic_unit, transcript_id_dataset)
    expected = "http://grch37.rest.ensembl.org/vep/human/hgvs/NM_170707.3:c.745C>T?content-type=application/json;"
    assert actual_identifier == expected
    assert isinstance(actual_task, HttpAnnotationTask)

def test_extract_annotations_from_response(http_annotation_task_many_datasets, transcript_annotation_response):
    """ Tests the annotation task extraction function """
    actual = http_annotation_task_many_datasets.extract(transcript_annotation_response)

    transcripts = list(actual.keys())

    first_transcript = transcripts[0]
    second_transcript = transcripts[1]

    assert len(actual) == 2
    assert first_transcript == 'NM_001017980.4'
    assert second_transcript == 'NM_001363810.1'

    assert len(actual[first_transcript]) == 3

    assert 'SIFT Prediction' in actual[second_transcript]

def test_annotation_extraction_recurse(annotation_extraction_recurse_fixtures):
    """ Tests the annotation task recursive helper function for extracting specific pieces of data from a response """
    data, attrs, dataset, annotations = annotation_extraction_recurse_fixtures

    actual = recurse(data, attrs, dataset, annotations)

    actual_keys_list = list(actual.keys())

    first_transcript = actual_keys_list[0]
    second_transcript = actual_keys_list[1]

    assert first_transcript == 'NM_001017980.4'
    assert second_transcript == 'NM_001363810.1'

    assert 'SIFT Score' in actual[first_transcript]
    assert actual[second_transcript]['SIFT Score']['value'] == 0.01

@pytest.fixture(name="hgvs_variant_genomic_unit")
def fixture_genomic_unit():
    """Returns the genomic unit 'NM_170707.3:c.745C>T' to be annotated"""
    return {
        "unit": "NM_170707.3:c.745C>T",
        "genomic_unit_type": GenomicUnitType.HGVS_VARIANT,
    }

@pytest.fixture(name="http_annotation_task_empty")
def fixture_http_annotation_empty(hgvs_variant_genomic_unit):
    """Returns an HTTP annotation task with not datasets appended"""
    return HttpAnnotationTask(hgvs_variant_genomic_unit)

@pytest.fixture(name="transcript_id_dataset")
def fixture_transcript_id_dataset(annotation_collection):
    """
    Returns the dict of the transcript_id dataset
    """
    return annotation_collection.find_by_data_set("transcript_id")

@pytest.fixture(name="http_annotation_transcript_id")
def fixture_http_annotation_transcript_id(http_annotation_task_empty, transcript_id_dataset):
    """An HTTP annotation task with a single dataset"""
    http_annotation_task_empty.append(transcript_id_dataset)
    return http_annotation_task_empty

@pytest.fixture(name="transcript_datasets_json")
def fixture_transcript_related_datasets(annotation_collection):
    """
    Returns the annotation collection for the configuration to verify
    annotation tasks are created according to the configuration
    """
    return list(
        filter(
            lambda x: (
                x["data_set"] == "transcript_id" or x["data_set"] == "SIFT Prediction" or x["data_set"] == "SIFT Score"
            ),
            annotation_collection.all(),
        )
    )

@pytest.fixture(name="http_annotation_task_many_datasets")
def fixture_http_annotation_many_datasets(http_annotation_task_empty, transcript_datasets_json):
    """An annotation task with many transcript datasets appeneded."""
    for dataset_json in transcript_datasets_json:
        http_annotation_task_empty.append(dataset_json)
    return http_annotation_task_empty

@pytest.fixture(name="annotation_extraction_recurse_fixtures")
def fixture_annotation_extraction_recurse():
    """ The components necessary for the recursive function to extract the data """
    http_response_data = {
            "transcript_consequences": [
                {
                    "transcript_id":"NM_001017980.4",
                    "sift_score":0.02,
                },
                {
                    "sift_score":0.01,
                    "transcript_id":"NM_001363810.1",
                }
            ],
        }

    desired_attribute = ["transcript_consequences[]", "sift_score"]

    transcript_dataset = {
        "data_set": "SIFT Score",
        "data_source": "Ensembl",
        "genomic_unit_type": "hgvs_variant",
        "annotation_source_type": "http",
        "url": "http://grch37.rest.ensembl.org/vep/human/hgvs/{hgvs_variant}?content-type=application/json",
        "query_param": "",
        "attribute": "transcript_consequences[].sift_score"
    }

    annotations = {}

    return http_response_data, desired_attribute, transcript_dataset, annotations
