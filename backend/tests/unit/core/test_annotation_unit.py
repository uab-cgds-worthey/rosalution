"""Tests for annotation unit class"""
from unittest.mock import Mock
import pytest

from src.core.annotation_unit import AnnotationUnit


def test_annotation_unit_gets_missing_dependencies(annotation_unit_lmna):
    """Verifies if the annotation unit's dataset dependencies are being returned as expected"""
    actual = annotation_unit_lmna.get_missing_dependencies()
    assert actual == ['HGNC_ID']


def test_annotation_unit_ready_for_annotation(annotation_unit_lmna):
    """Verifies if the annotation unit is ready for annotation"""

    missing = annotation_unit_lmna.get_missing_dependencies()
    missing_dependency = missing[0]
    mock_genomic_unit_collection = Mock()
    mock_genomic_unit_collection.find_genomic_unit_annotation_value = Mock()
    annotation_value = mock_genomic_unit_collection.find_genomic_unit_annotation_value(
        annotation_unit_lmna.genomic_unit, missing_dependency
    )

    actual = annotation_unit_lmna.ready_for_annotation(annotation_value, missing_dependency)
    assert actual is True


def test_annotation_unit_should_continue_annotation(annotation_unit_lmna):
    """Verifies if the annotation unit should continue annotation"""
    actual_missing_dependencies, actual_logger_message = annotation_unit_lmna.should_continue_annotation()
    assert actual_missing_dependencies == ""
    assert actual_logger_message == '%s Delaying Annotation, Missing Dependency...'


@pytest.fixture(name="annotation_unit_lmna")
def fixture_annotation_unit():
    """Returns the annotation unit for the genomic unit LMNA and the dataset Clingen gene url"""
    genomic_unit = {'unit': 'LMNA'}
    dataset = {
        "data_set": "ClinGen_gene_url", "data_source": "Rosalution", "genomic_unit_type": "gene",
        "annotation_source_type": "forge", "base_string": "https://search.clinicalgenome.org/kb/genes/{HGNC_ID}",
        "attribute": "{ \"ClinGen_gene_url\": .ClinGen_gene_url }", "dependencies": ["HGNC_ID"]
    }
    return AnnotationUnit(genomic_unit, dataset)
