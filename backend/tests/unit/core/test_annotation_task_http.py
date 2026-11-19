"""Tests Annotation Tasks and the creation of them"""
import pytest

from src.core.annotation_task import AnnotationTaskFactory, HttpAnnotationTask
from src.core.annotation_unit import AnnotationUnit


def test_http_annotation_task_build_url(http_annotation_transcript_id):
    """Verifies that the HTTP annotation task creates the base url using the 'url' and the genomic unit"""
    actual = http_annotation_transcript_id.build_url()

    assert (
        actual ==
        "http://grch37.rest.ensembl.org/vep/human/hgvs/NM_170707.3:c.745C>T?content-type=application/json;refseq=1;"
    )
    # This link cannot be shortened, will just disable for this one due to the nature of the long URL dependency


def test_http_annotation_task_build_url_with_dependency(http_annotation_task_gene):
    """Verifies that the HTTP annotation task builds the URL that includes depdencies"""
    actual = http_annotation_task_gene.build_url()
    assert actual == "https://hpo.jax.org/api/hpo/gene/45614"


def test_annotation_task_create_http_task(hgvs_variant_annotation_unit):
    """Verifies that the annotation task factory creates the correct annotation task according to the dataset type"""
    actual_task = AnnotationTaskFactory.create_annotation_task(hgvs_variant_annotation_unit)
    assert isinstance(actual_task, HttpAnnotationTask)


def test_annotation_extraction_for_transcript_id_dataset(http_annotation_transcript_id, transcript_annotation_response):
    """Verifying genomic unit extraction for a transcript using the the transcript ID dataset"""
    actual_extractions = http_annotation_transcript_id.extract(transcript_annotation_response)
    assert len(actual_extractions) == 2
    assert {
        'data_set': 'transcript_id', 'data_source': 'Ensembl', 'version': '', 'value': 'NM_001017980.4',
        'transcript_id': 'NM_001017980.4'
    } in actual_extractions

    assert {
        'data_set': 'transcript_id', 'data_source': 'Ensembl', 'version': '', 'value': 'NM_001363810.1',
        'transcript_id': 'NM_001363810.1'
    } in actual_extractions


def test_annotation_extraction_for_polyphen_prediction_transcript_dataset(
    http_annotation_polyphen_prediction, transcript_annotation_response
):
    """Verifying genomic unit extraction for a transcript using the the transcript ID dataset"""
    actual_extractions = http_annotation_polyphen_prediction.extract(transcript_annotation_response)
    assert len(actual_extractions) == 2

    actual_nm_001017980_extraction = next(
        (annotation for annotation in actual_extractions if annotation['transcript_id'] == 'NM_001017980.4'), None
    )

    actual_nm_001363810_extraction = next(
        (annotation for annotation in actual_extractions if annotation['transcript_id'] == 'NM_001363810.1'), None
    )

    assert actual_nm_001017980_extraction['value'] == 'possibly_damaging'
    assert actual_nm_001363810_extraction['value'] == 'probably_damaging'


def test_annotation_extraction_for_genomic_unit(http_annotation_task_gene, hpo_annotation_response):
    """Verifying genomic unit extraction for a gene using the HPO dataset"""
    actual_extractions = http_annotation_task_gene.extract(hpo_annotation_response)
    assert len(actual_extractions) == 1
    assert {
        'data_set': 'HPO', 'data_source': 'HPO', 'version': '',
        'value': ['Myopathy, X-linked, With Excessive Autophagy']
    } in actual_extractions


def test_annotation_extraction_value_error_exception(http_annotation_task_gene, hpo_annotation_response):
    """
    Verifying annotation failure does not cause crash in application during extraction. Removes the expected value
    in the json to force jq parse error to more closely simulate the failure instead of mocking the jq response to fail.
    """

    del hpo_annotation_response['diseaseAssoc']

    with pytest.raises(RuntimeError) as runtime_error:
        http_annotation_task_gene.extract(hpo_annotation_response)
        assert 'Failed to annotate "HPO"' in runtime_error


## Fixtures ##


@pytest.fixture(name="transcript_id_dataset")
def fixture_transcript_id_dataset():
    """
    Returns the dict of the transcript_id dataset
    """
    return {
        "data_set": "transcript_id",
        "data_source": "Ensembl",
        "genomic_unit_type": "hgvs_variant",
        "transcript": True,
        "annotation_source_type": "http",
        "url": "http://grch37.rest.ensembl.org/vep/human/hgvs/{hgvs_variant}?content-type=application/json;refseq=1;",
        "attribute": ".[].transcript_consequences[] | { transcript_id: .transcript_id }",
    }


@pytest.fixture(name="hgvs_variant_annotation_unit")
def fixture_hgvs_variant_annotation_unit(hgvs_variant_genomic_unit_for_annotation_tasks, transcript_id_dataset):
    """
    Returns the annotation unit with hgvs_variant genomic unit and transcript_id dataset
    """
    annotation_unit = AnnotationUnit(hgvs_variant_genomic_unit_for_annotation_tasks, transcript_id_dataset)
    return annotation_unit


@pytest.fixture(name="http_annotation_transcript_id")
def fixture_http_annotation_transcript_id(hgvs_variant_genomic_unit_for_annotation_tasks, transcript_id_dataset):
    """An HTTP annotation task with a single dataset"""
    annotation_unit = AnnotationUnit(hgvs_variant_genomic_unit_for_annotation_tasks, transcript_id_dataset)
    task = HttpAnnotationTask(annotation_unit)
    return task


@pytest.fixture(name="polyphen_prediction_dataset")
def fixture_polyphen_prediction_dataset():
    """
    Returns the dict of the polyphen_prediction dataset
    """
    return {
        "data_set": "Polyphen Prediction",
        "data_source": "Ensembl",
        "genomic_unit_type": "hgvs_variant",
        "transcript": True,
        "annotation_source_type": "http",
        "url": "http://grch37.rest.ensembl.org/vep/human/hgvs/{hgvs_variant}?content-type=application/json;refseq=1;",
        "attribute":
            ".[].transcript_consequences[] | \
            { polyphen_prediction: .polyphen_prediction,transcript_id: .transcript_id }",
    }


@pytest.fixture(name="http_annotation_polyphen_prediction")
def fixture_http_annotation_polyphen_prediction(
    hgvs_variant_genomic_unit_for_annotation_tasks, polyphen_prediction_dataset
):
    """An HTTP annotation task with a single dataset"""
    annotation_unit = AnnotationUnit(hgvs_variant_genomic_unit_for_annotation_tasks, polyphen_prediction_dataset)
    task = HttpAnnotationTask(annotation_unit)
    return task
