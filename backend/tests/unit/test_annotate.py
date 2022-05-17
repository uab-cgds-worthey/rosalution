"""Tests to verify annotation tasks"""
from unittest.mock import Mock, patch
import queue
import pytest
from src.enums import GenomicUnitType

from src.annotation import AnnotationTask
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

def test_annotation_task_base_url_if_not_datasets(cpam0046_hgvs_genomic_unit):
    """Verifies that an annotation task can return what the base url is for a genomic unit"""
    task = AnnotationTask()
    actual = task.base_url(cpam0046_hgvs_genomic_unit)
    assert actual is None

def test_annotation_task_base_url_with_datasets(transcript_id_dataset, cpam0046_hgvs_genomic_unit):
    """
    Verifies that an annotation task returns the base_url
    """
    task = AnnotationTask()
    task.append(DataSetSource(**transcript_id_dataset))
    actual = task.base_url(cpam0046_hgvs_genomic_unit)
    assert actual == "http://grch37.rest.ensembl.org/vep/human/hgvs/NM_170707.3:c.745C>T?content-type=application/json;"
    
def test_annotation_task_base_url_man_datasets(transcript_datasets, cpam0046_hgvs_genomic_unit):
    task = AnnotationTask()
    for dataset in transcript_datasets:
      task.append(DataSetSource(**dataset))
    actual = task.base_url(cpam0046_hgvs_genomic_unit)
    assert actual == "http://grch37.rest.ensembl.org/vep/human/hgvs/NM_170707.3:c.745C>T?content-type=application/json;"
    
  
@pytest.fixture(name="cpam0046_hgvs_genomic_unit")
def fixture_cpam0046_hgvs_genomic_unit(cpam0046_analysis):
    """
    Returns the HGVS variant within the CPAM0046 analysis.
    """
    genomic_units = cpam0046_analysis.units_to_annotate()
    unit = {}
    for genomic_unit in genomic_units:
        if genomic_unit['type'] == GenomicUnitType.HGVS_VARIANT:
          unit = genomic_unit
    
    return unit  

@pytest.fixture(name='cpam0046_analysis')
def fixture_cpam0046_analysis(analysis_collection):
    """Returns the Analysis for CPAM0046 to verify creating annotation tasks"""
    analysis_json = analysis_collection.find_by_name('CPAM0046')
    return Analysis(**analysis_json)


@pytest.fixture(name="analysis_collection")
def fixture_analysis_collection():
    """Returns the analysis collection to be mocked"""

    return AnalysisCollection()


@pytest.fixture(name="transcript_id_dataset")
def fixture_transcript_id_dataset(annotation_collection):
    """
    Returns the dict of the transcript_id dataset
    """
    return annotation_collection.find_by_data_set('transcript_id')


@pytest.fixture(name="transcript_datasets")
def fixture_transcript_related_datasets(annotation_collection):
    """
    Returns the annotation collection for the configuration to verify
    annotation tasks are created according to the configuration
    """
    return list(filter(lambda x: (x['data_set'] == "transcript_id" or x['data_set'] == "SIFT Prediction" or x['data_set'] == "SIFT Score"), annotation_collection))


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
