"""Tests to verify annotation tasks"""
from unittest.mock import Mock, patch
import pytest

from src.core.annotation import AnnotationService
from src.enums import GenomicUnitType


def test_queuing_annotations_for_genomic_units(cpam0046_analysis, annotation_collection):
    """Verifies annotations are queued according to the specific genomic units"""
    annotation_service = AnnotationService(annotation_collection)
    mock_queue = Mock()
    annotation_service.queue_annotation_tasks(cpam0046_analysis, mock_queue)
    assert mock_queue.put.call_count == 29

# Patching the temporary helper method that is writing to a file, this will be
# removed once that helper method is no longer needed for the development

# The patched method sare done provided in reverse order within the test param arguments.  Was accidently getting
# logging mock results instead of non task type annotations.  Was causing major failures in verifying values
@patch("src.core.annotation.log_to_file")
@patch("src.core.annotation_task.AnnotationTaskInterface.extract")
@patch("src.core.annotation_task.ForgeAnnotationTask.annotate")
@patch("src.core.annotation_task.HttpAnnotationTask.annotate")
@patch("src.core.annotation_task.NoneAnnotationTask.annotate")
def test_processing_cpam0046_annotation_tasks(
    none_task_annotate,
    http_task_annotate,
    forge_task_annotate,
    annotate_extract_mock,
    log_to_file_mock,
    cpam0046_annotation_queue
):  # pylint: disable=unused-argument
    """Verifies that each item on the annotation queue is read and executed"""
    flag = {'dependency_flag_passed': False}
    def dependency_mock_side_effect(*args, **kwargs): # pylint: disable=unused-argument
        query, value = args  # pylint: disable=unused-variable
        if value != 'HGNC_ID':
            return 'kfldjsfds'

        if flag['dependency_flag_passed']:
            return 'klfjdsfdsfa'

        flag['dependency_flag_passed'] = True
        return None

    mock_genomic_unit_collection = Mock()
    mock_genomic_unit_collection.find_genomic_unit_annotation_value = Mock()
    mock_genomic_unit_collection.find_genomic_unit_annotation_value.side_effect = dependency_mock_side_effect
    mock_genomic_unit_collection.annotation_exist.return_value = False

    assert not cpam0046_annotation_queue.empty()
    AnnotationService.process_tasks(cpam0046_annotation_queue, mock_genomic_unit_collection)
    assert cpam0046_annotation_queue.empty()

    assert http_task_annotate.call_count == 23
    assert none_task_annotate.call_count == 0
    assert forge_task_annotate.call_count == 6

    assert annotate_extract_mock.call_count == 29

@patch("src.core.annotation.log_to_file")
@patch("src.core.annotation_task.AnnotationTaskInterface.extract",return_value=[{
        'data_set': 'mock_datset',
        'data_source': 'mock_source',
        'version': '0.0',
        'value': '9000'
    }])
@patch("src.core.annotation_task.ForgeAnnotationTask.annotate")
@patch("src.core.annotation_task.HttpAnnotationTask.annotate")
@patch("src.core.annotation_task.NoneAnnotationTask.annotate")
def test_processing_cpam0002_annotations_tasks(
    none_task_annotate,
    http_task_annotate,
    forge_task_annotate,
    annotate_extract_mock,
    log_to_file_mock,
    cpam0002_annotation_queue
):  # pylint: disable=unused-argument
    """
        Verifies that the annotation collection is being sent the proper amount of extracted annotations for
        CPAM analysis 0002
    """

    mock_genomic_unit_collection = Mock()
    mock_genomic_unit_collection.annotation_exist.return_value = False

    AnnotationService.process_tasks(cpam0002_annotation_queue, mock_genomic_unit_collection)

    assert http_task_annotate.call_count == 23
    assert forge_task_annotate.call_count == 6
    assert none_task_annotate.call_count == 0

    assert annotate_extract_mock.call_count == 29

    mock_genomic_unit_collection.annotate_genomic_unit.assert_called()

@pytest.fixture(name="cpam0046_hgvs_variant_json")
def fixture_cpam0046_hgvs_variant(cpam0046_analysis):
    """Returns the HGVS variant within the CPAM0046 analysis."""
    genomic_units = cpam0046_analysis.units_to_annotate()
    unit = {}
    for genomic_unit in genomic_units:
        if genomic_unit["type"] == GenomicUnitType.HGVS_VARIANT:
            unit = genomic_unit

    return unit
