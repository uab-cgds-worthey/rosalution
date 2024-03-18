"""Tests for annotation unit class"""
import pytest

from src.core.annotation_unit import AnnotationUnit


def test_annotation_unit_gets_missing_dependencies(annotation_unit_lmna):
    """Verifies if the annotation unit's dataset dependencies are being returned as expected"""
    actual = annotation_unit_lmna.get_missing_dependencies()
    assert actual == ['HGNC_ID']


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
