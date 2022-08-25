"""Tests Annotation Tasks and the creation of them"""
import pytest
from src.enums import GenomicUnitType
from src.annotation_task import AnnotationTaskFactory, HttpAnnotationTask, transcript_annotation_extration


def test_http_annotation_base_url(http_annotation_transcript_id):
    """Verifies if the HTTP annotation creates the base url using the url and genomic_unit as expected."""
    actual = http_annotation_transcript_id.base_url()
    assert actual == "http://grch37.rest.ensembl.org/vep/human/hgvs/NM_170707.3:c.745C>T?content-type=application/json;"


def test_http_annotation_task_build_url(http_annotation_transcript_id):
    """Verifies that the HTTP annotation task creates the base url using the 'url' and the genomic unit"""
    actual = http_annotation_transcript_id.build_url()
    assert actual == "http://grch37.rest.ensembl.org/vep/human/hgvs/NM_170707.3:c.745C>T?content-type=application/json;refseq=1;"  # pylint: disable=line-too-long
    # This link cannot be shortened, will just disable for this one due to the nature of the long URL dependency

def test_http_annotation_task_build_url_with_dependency(http_annotation_task_gene):
    """Verifies that the HTTP annotation task builds the URL that includes depdencies"""
    actual = http_annotation_task_gene.build_url()
    assert actual == "https://hpo.jax.org/api/hpo/gene/45614"

def test_annotation_task_create_http_task(hgvs_variant_genomic_unit, transcript_id_dataset):
    """Verifies that the annotation task factory creates the correct annotation task according to the dataset type"""
    actual_task = AnnotationTaskFactory.create(
        hgvs_variant_genomic_unit, transcript_id_dataset)
    assert isinstance(actual_task, HttpAnnotationTask)


def test_transcript_annotation_extraction():
    """
    When jq extracts annotations from an array, it can yield many results in an array. This tests that proper result
    are associated with the correct transcript and returns an updated annotation unit.
    """
    annotation_unit = {
        "data_set": "SIFT Prediction",
        "data_source": "Ensembl",
        "version": "",
        "value": "",
    }

    transcript_result = {'sift_prediction': 'deleterious',
                         'transcript_id': 'NM_001363810.1'}

    actual = transcript_annotation_extration(annotation_unit, transcript_result)

    transcript_annotation_unit = {
        'data_set': 'SIFT Prediction',
        'data_source': 'Ensembl',
        'version': '',
        'value': 'deleterious',
        'transcript_id': 'NM_001363810.1'
    }

    assert actual == transcript_annotation_unit

## Fixtures ##

@pytest.fixture(name="gene_hpo_dataset")
def fixture_gene_hpo_dataset():
    """
    Returns the dict of the HPO dataset that has a dependency
    """
    return   {
        "data_set": "HPO",
        "data_source": "HPO",
        "genomic_unit_type": "gene",
        "annotation_source_type": "http",
        "url": "https://hpo.jax.org/api/hpo/gene/{Entrez Gene Id}",
        "query_param": "",
        "dependencies": ["Entrez Gene Id"]
    }

@pytest.fixture(name="gene_genomic_unit")
def fixture_gene_genomic_unit():
    """Returns the genomic unit 'VMA21' to be annotated"""
    return {
        "unit": "VMA21",
        "Entrez Gene Id": "45614",
        "genomic_unit_type": GenomicUnitType.GENE,
    }

@pytest.fixture(name="http_annotation_task_gene")
def fixture_http_annotation_empty(gene_genomic_unit, gene_hpo_dataset):
    """Returns an HTTP annotation taskd"""
    task = HttpAnnotationTask(gene_genomic_unit)
    task.set(gene_hpo_dataset)
    return task

@pytest.fixture(name="hgvs_variant_genomic_unit")
def fixture_genomic_unit():
    """Returns the genomic unit 'NM_170707.3:c.745C>T' to be annotated"""
    return {
        "unit": "NM_170707.3:c.745C>T",
        "genomic_unit_type": GenomicUnitType.HGVS_VARIANT,
    }


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
        "url": "http://grch37.rest.ensembl.org/vep/human/hgvs/{hgvs_variant}?content-type=application/json;",
        "query_param": "refseq=1;",
        "attribute": "transcript_consequences[].transcript_id"
    }


@pytest.fixture(name="http_annotation_transcript_id")
def fixture_http_annotation_transcript_id(hgvs_variant_genomic_unit, transcript_id_dataset):
    """An HTTP annotation task with a single dataset"""
    task = HttpAnnotationTask(hgvs_variant_genomic_unit)
    task.set(transcript_id_dataset)
    return task


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
