"""Tests to verify annotation tasks"""
from unittest.mock import Mock, patch
import queue
import pytest

from src.core.analysis import Analysis
from src.core.data_set_source import DataSetSource
from src.repository.analysis_collection import AnalysisCollection
from src.repository.annotation_collection import AnnotationCollection
from src.annotation import AnnotationService


def test_queuing_annotations_for_genomic_units(cpam0046_analysis, annotation_collection):
    """Verifies annotations are queued according to the specific genomic units"""
    annotation_service = AnnotationService(annotation_collection)
    mock_queue = Mock()
    annotation_service.queue_annotation_tasks(cpam0046_analysis, mock_queue)
    assert mock_queue.put.call_count == 19

# Patching the temporary helper method that is writing to a file, this will be
# removed once that helper method is no longer needed for the development


# The patch requires that the 'mock' being created must be the first argument
# so removing it causes the test to not run.  Also is unable to detect
# the mock overide of the 'annotate' function on DataSetSource is valid either.
@patch('src.annotation.log_to_file')
def test_processing_annotation_tasks(log_to_file_mock, annotation_queue): #pylint: disable=unused-argument
    """Verifies that each item on the annotation queue is read and executed """
    assert not annotation_queue.empty()
    DataSetSource.annotate = Mock()
    AnnotationService.process_tasks(annotation_queue)
    assert annotation_queue.empty()
    assert DataSetSource.annotate.call_count == 19 # pylint: disable=no-member


@pytest.fixture(name='cpam0046_analysis')
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


@pytest.fixture(name="annotation_queue")
def fixture_annotation_queue(annotation_collection, cpam0046_analysis):
    """
    Returns an thread-safe annotation queue with tasks
    """
    annotation_service = AnnotationService(annotation_collection)
    test_queue = queue.Queue()
    annotation_service.queue_annotation_tasks(cpam0046_analysis, test_queue)
    return test_queue
