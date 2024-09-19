"""Tests for annotation unit class"""
import pytest

from src.core.annotation_unit import AnnotationUnit


def test_annotation_unit_gets_missing_dependencies(annotation_unit_lmna):
    """Verifies if the annotation unit's dataset dependencies are being returned as expected"""
    actual = annotation_unit_lmna.get_missing_dependencies()
    assert actual == ['HGNC_ID']


def test_annotation_unit_ready_for_annotation(annotation_unit_has_dependency):
    """Verifies if the annotation unit is ready for annotation"""

    actual = annotation_unit_has_dependency.conditions_met_to_gather_annotation()
    assert actual is True


def test_annotation_unit_not_ready_for_annotation(annotation_unit_lmna):
    """Verifies if the annotation unit is not ready for annotation"""

    actual = annotation_unit_lmna.conditions_met_to_gather_annotation()
    assert actual is False


def test_annotation_unit_should_continue_annotation(annotation_unit_lmna):
    """
    Verifies if the annotation unit should continue annotation for both cases
    of annotation_unit with delay_count not exceeded and exceeded.
    """

    assert annotation_unit_lmna.should_continue_annotation()


def test_annotation_unit_should_not_continue_annotation(annotation_unit_lmna_exceeded_delay_count):
    """
    Verifies if the annotation unit should not continue annotation for the case
    of annotation_unit with exceeded delay_count.
    """

    assert not annotation_unit_lmna_exceeded_delay_count.should_continue_annotation()


@pytest.fixture(name="annotation_unit_lmna")
def fixture_annotation_unit_lmna():
    """Returns the annotation unit for the genomic unit LMNA and the dataset Clingen gene url"""
    genomic_unit = {'unit': 'LMNA'}
    dataset = {
        "data_set": "ClinGen_gene_url", "data_source": "Rosalution", "genomic_unit_type": "gene",
        "annotation_source_type": "forge", "base_string": "https://search.clinicalgenome.org/kb/genes/{HGNC_ID}",
        "attribute": "{ \"ClinGen_gene_url\": .ClinGen_gene_url }", "dependencies": ["HGNC_ID"], "delay_count": 5
    }
    return AnnotationUnit(genomic_unit, dataset)


@pytest.fixture(name="annotation_unit_has_dependency")
def fixture_annotation_unit_lmna_has_dependencies(annotation_unit_lmna):
    """Provides annotation unit that has all of its dependencies gathered"""
    annotation_unit_lmna.set_annotation_for_dependency("HGNC_ID", "FAKE_HGNC_ID_VALUE")
    return annotation_unit_lmna


@pytest.fixture(name="annotation_unit_lmna_exceeded_delay_count")
def fixture_annotation_unit_lmna_with_annotated_dependency(annotation_unit_lmna):
    """Returns the annotation unit for the genomic unit LMNA and the dataset Clingen gene url"""
    annotation_unit_lmna.dataset['delay_count'] = 10
    return annotation_unit_lmna
