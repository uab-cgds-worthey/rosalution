import pytest

from src.repository.analysis_collection import AnnotationCollection
from src.enums import GenomicUnitType


def test_get_datasets_configuration(annotation_collection):
  types = set(GenomicUnitType.GENE, GenomicUnitType.HGVS_VARIANT)
  datasets = annotation_collection.getDataSetsConfiguration(types)


@pytest.fixture
def annotation_collection():
  return AnnotationCollection()
