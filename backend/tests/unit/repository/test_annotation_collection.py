"""Tests to verify dataset configuration is returned"""
# from unittest.mock import Mock
import pytest

from src.repository.annotation_collection import AnnotationCollection
from src.enums import GenomicUnitType

# from src.utils import read_fixture


def test_get_datasets_configuration_by_type(annotation_collection):
    """Tests getting the datasets for the provided types of genomic units"""
    types = set({GenomicUnitType.GENE, GenomicUnitType.HGVS_VARIANT})
    datasets = annotation_collection.datasets_to_annotate_by_type(types)
    assert len(datasets) == 19

def test_get_datasets_to_annotate_for_units(annotation_collection, genomic_units_for_annotation):
    """Tests if the configuration for datasets is return as expected"""
    actual_configuration = annotation_collection.datasets_to_annotate_for_units(genomic_units_for_annotation)
    assert len(actual_configuration['gene']) == 9
    assert len(actual_configuration['hgvs_variant']) == 10


@pytest.fixture(name='genomic_units_for_annotation')
def fixture_genomic_units():
    """Fixture for list of genomic units"""
    return [{
      'type': GenomicUnitType.GENE,
      'unit': 'DMD'
    }, {
      'type': GenomicUnitType.GENE,
      'unit': 'VMA21'
    }, {
      'type': GenomicUnitType.HGVS_VARIANT,
      'unit': 'NM_170707.3:c.745C>T'
    }]

@pytest.fixture(name='annotation_collection')
def fixture_annotation_collection():
    """Fixture for the annotation collection"""
    return AnnotationCollection()
    # mock_collection = Mock()
    # mock_collection.find = Mock( return_value = read_fixture("annotation-sources.json") )
    # return AnnotationCollection(mock_collection)
