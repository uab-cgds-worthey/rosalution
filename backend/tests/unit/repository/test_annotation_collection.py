"""Tests to verify dataset configuration is returned"""
# from unittest.mock import Mock
import pytest

from src.repository.annotation_collection import AnnotationCollection
from src.enums import GenomicUnitType

# from src.utils import read_fixture


def test_get_datasets_configuration(annotation_collection):
    """Tests getting the datasets for the provided types of genomic units"""
    types = set({GenomicUnitType.GENE, GenomicUnitType.HGVS_VARIANT})
    datasets = annotation_collection.datasets_to_annotate(types)
    assert len(datasets) == 19


@pytest.fixture(name='annotation_collection')
def fixture_annotation_collection():
    """Fixture for the annotation collection"""
    return AnnotationCollection()
    # mock_collection = Mock()
    # mock_collection.find = Mock( return_value = read_fixture("annotation-sources.json") )
    # return AnnotationCollection(mock_collection)
