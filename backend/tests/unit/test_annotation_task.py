"""Tests Annotation Tasks and the creation of them"""
import pytest
from src.enums import GenomicUnitType
from src.annotation_task import AnnotationTaskFactory, HttpAnnotationTask


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


def test_http_annotation_task_base_url_many_datasets(http_annotation_task_many_datasets):
    """Verifies that the HTTP annotation task creates the base url using the 'url' and the genomic unit"""
    actual = http_annotation_task_many_datasets.base_url()
    assert actual == "http://grch37.rest.ensembl.org/vep/human/hgvs/NM_170707.3:c.745C>T?content-type=application/json;"


def test_http_annotation_task_build_url(http_annotation_task_many_datasets):
    """Verifies that the HTTP annotation task builds the complete URL including the base url and the query params"""
    actual = http_annotation_task_many_datasets.build_url()
    expected = "http://grch37.rest.ensembl.org/vep/human/hgvs/" \
        "NM_170707.3:c.745C>T?content-type=application/json;refseq=1;"
    assert actual == expected


def test_annotation_task_create_http_task(hgvs_variant_genomic_unit, transcript_id_dataset):
    """Verifies that the annotation task factory creates the correct annotation task according to the dataset type"""
    actual_identifier, actual_task = AnnotationTaskFactory.create(
        hgvs_variant_genomic_unit, transcript_id_dataset)
    expected = "http://grch37.rest.ensembl.org/vep/human/hgvs/NM_170707.3:c.745C>T?content-type=application/json;"
    assert actual_identifier == expected
    assert isinstance(actual_task, HttpAnnotationTask)


@pytest.fixture(name="hgvs_variant_genomic_unit")
def fixture_genomic_unit():
    """Returns the genomic unit 'NM_170707.3:c.745C>T' to be annotated"""
    return {
        "unit": "NM_170707.3:c.745C>T",
        "genomic_unit_type": GenomicUnitType.HGVS_VARIANT
    }


@pytest.fixture(name='http_annotation_task_empty')
def fixture_http_annotation_empty(hgvs_variant_genomic_unit):
    """Returns an HTTP annotation task with not datasets appended"""
    return HttpAnnotationTask(hgvs_variant_genomic_unit)


@pytest.fixture(name="transcript_id_dataset")
def fixture_transcript_id_dataset(annotation_collection):
    """
    Returns the dict of the transcript_id dataset
    """
    return annotation_collection.find_by_data_set('transcript_id')


@pytest.fixture(name='http_annotation_transcript_id')
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
    return list(filter(
        lambda x:
            (x['data_set'] == "transcript_id" or x['data_set'] ==
             "SIFT Prediction" or x['data_set'] == "SIFT Score"),
            annotation_collection.all()))


@pytest.fixture(name='http_annotation_task_many_datasets')
def fixture_http_annotation_many_datasets(http_annotation_task_empty, transcript_datasets_json):
    """An annotation task with many transcript datasets appeneded."""
    for dataset_json in transcript_datasets_json:
        http_annotation_task_empty.append(dataset_json)
    return http_annotation_task_empty
