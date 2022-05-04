"""Tests to verify dataset configuration is returned"""
import pytest

from src.repository.annotation_collection import AnnotationCollection
from src.enums import GenomicUnitType


def test_get_datasets_configuration(annotation_collection):
  types = set({GenomicUnitType.GENE, GenomicUnitType.HGVS_VARIANT})
  datasets = annotation_collection.datasets_configuration(types)
  assert len(datasets) == 19


@pytest.fixture(name="annotation_collection")
def fixture_annotation_collection():
  return AnnotationCollection()
