"""Tests to verify annotation tasks"""
import pytest

from src.core.analysis import Analysis
from src.repository.analysis_collection import AnalysisCollection
from src.repository.annotation_collection import AnnotationCollection
from src.annotation_service import AnnotationService


def test_queuing_annotations_for_genomic_units(analysis, annotation_collection):
    """Verifies annotations are queued according to the specific genomic units"""
    units_to_annotate = analysis.units_to_annotate()
    types_to_annotate = set(map(lambda x: x['type'], units_to_annotate))

    annotation_service = AnnotationService(annotation_collection)
    datasets_to_annotate = annotation_service.annotate(
        units_to_annotate, types_to_annotate)
    # print('called annotate')
    # print(datasets_to_annotate)
    assert true == false


@pytest.fixture(name="analysis")
def fixture_cpam0046_analysis(analysis_collection):
    """Returns the Analysis for CPAM0046 to verify creating annotation tasks"""
    analysis_json = analysis_collection.find_by_name('CPAM0046')
    return Analysis(**analysis_json)


@pytest.fixture(name="analysis_collection")
def fixture_analysis_collection():
    """Returns the analysis collection to be mocked"""
    return AnalysisCollection()


@pytest.fixture(name="annotation_collection")
def fixture_annotation_collection():
    """
    Returns the annotation collection for the configuration to verify
    annotation tasks are created according to the configuration
    """
    return AnnotationCollection()
