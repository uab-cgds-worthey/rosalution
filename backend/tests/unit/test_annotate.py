"""Tests to verify annotation tasks"""
from unittest.mock import Mock, patch
import pytest

from src.annotation_task import HttpAnnotationTask, NoneAnnotationTask
from src.enums import GenomicUnitType
from src.annotation import AnnotationService

def test_queuing_annotations_for_genomic_units(cpam0046_analysis, annotation_collection):
    """Verifies annotations are queued according to the specific genomic units"""
    annotation_service = AnnotationService(annotation_collection)
    mock_queue = Mock()
    annotation_service.queue_annotation_tasks(cpam0046_analysis, mock_queue)
    assert mock_queue.put.call_count == 20

# Patching the temporary helper method that is writing to a file, this will be
# removed once that helper method is no longer needed for the development

# The patch requires that the 'mock' being created must be the first argument
# so removing it causes the test to not run.  Also is unable to detect
# the mock overide of the 'annotate' function on DataSetSource is valid either.
@patch("src.annotation.log_to_file")
def test_processing_annotation_tasks(log_to_file_mock, cpam0046_annotation_queue):  # pylint: disable=unused-argument
    """Verifies that each item on the annotation queue is read and executed"""
    mock_genomic_unit_collection = Mock()
    assert not cpam0046_annotation_queue.empty()
    HttpAnnotationTask.annotate = Mock(return_value={})
    NoneAnnotationTask.annotate = Mock()
    AnnotationService.process_tasks(cpam0046_annotation_queue, mock_genomic_unit_collection)
    assert cpam0046_annotation_queue.empty()
    assert HttpAnnotationTask.annotate.call_count == 2  # pylint: disable=no-member
    assert NoneAnnotationTask.annotate.call_count == 8  # pylint: disable=no-member

@patch("src.annotation.log_to_file")
def test_processing_cpam0002_annotations_tasks(
        log_to_file_mock, cpam0002_annotation_queue, transcript_annotation_response
    ): # pylint: disable=unused-argument
    """
        Verifies that the annotation collection is being sent the proper amount of extracted annotations for
        CPAM analysis 0002
    """

    mock_genomic_unit_collection = Mock()

    HttpAnnotationTask.annotate = Mock(return_value=transcript_annotation_response)
    NoneAnnotationTask.annotate = Mock()

    AnnotationService.process_tasks(cpam0002_annotation_queue, mock_genomic_unit_collection)

    assert HttpAnnotationTask.annotate.call_count == 2 # pylint: disable=no-member
    assert NoneAnnotationTask.annotate.call_count == 14 # pylint: disable=no-member
    assert mock_genomic_unit_collection.annotate_genomic_unit.call_count == 12

@pytest.fixture(name="cpam0046_hgvs_variant_json")
def fixture_cpam0046_hgvs_variant(cpam0046_analysis):
    """Returns the HGVS variant within the CPAM0046 analysis."""
    genomic_units = cpam0046_analysis.units_to_annotate()
    unit = {}
    for genomic_unit in genomic_units:
        if genomic_unit["type"] == GenomicUnitType.HGVS_VARIANT:
            unit = genomic_unit

    return unit
