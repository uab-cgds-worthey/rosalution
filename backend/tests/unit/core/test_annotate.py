"""Tests to verify annotation tasks"""
from unittest.mock import Mock, patch
import pytest

from src.core.annotation import AnnotationService
from src.enums import GenomicUnitType
from src.repository.genomic_unit_collection import GenomicUnitCollection


def test_queuing_annotations_for_genomic_units(cpam0046_analysis, annotation_config_collection):
    """Verifies annotations are queued according to the specific genomic units"""
    annotation_service = AnnotationService(annotation_config_collection)
    mock_queue = Mock()
    annotation_service.queue_annotation_tasks(cpam0046_analysis, mock_queue)
    assert mock_queue.put.call_count == 7

    for put_call in mock_queue.put.call_args_list:
        print(put_call)
    actual_queued_genomic_units = [put_call.args[0].genomic_unit['unit'] for put_call in mock_queue.put.call_args_list]

    assert "NM_170707.3:c.745C>T" in actual_queued_genomic_units


def test_processing_cpam0046_annotation_tasks(process_cpam0046_tasks):
    """Verifies that each item on the annotation queue is read and executed"""
    assert process_cpam0046_tasks['http'].call_count == 5
    assert process_cpam0046_tasks['none'].call_count == 0
    assert process_cpam0046_tasks['forge'].call_count == 2

    assert process_cpam0046_tasks['extract'].call_count == 7


def test_processing_cpam0002_annotations_tasks(process_cpam0002_tasks):
    """
        Verifies that the annotation collection is being sent the proper amount of extracted annotations for
        CPAM analysis 0002
    """

    assert process_cpam0002_tasks['http'].call_count == 5
    assert process_cpam0002_tasks['none'].call_count == 0
    assert process_cpam0002_tasks['forge'].call_count == 2

    assert process_cpam0002_tasks['extract'].call_count == 7

    process_cpam0002_tasks['genomic_unit_collection'].annotate_genomic_unit.assert_called()


def test_processing_cpam0002_annotation_tasks_for_datasets_with_dependencies(process_cpam0002_tasks):
    """Tests that the dependencies will put the annotation task back onto the processing queue when its missing a depedency"""

    assert process_cpam0002_tasks['genomic_unit_collection'].find_genomic_unit_annotation_value.call_count == 4


def test_processing_cpam0002_datasets_with_dependencies(cpam0002_annotation_queue, process_cpam0002_tasks):
    assert cpam0002_annotation_queue.empty()

    assert process_cpam0002_tasks['http'].call_count == 5
    assert process_cpam0002_tasks['none'].call_count == 0
    assert process_cpam0002_tasks['forge'].call_count == 2

    assert process_cpam0002_tasks['extract'].call_count == 7


def test_processing_cpam0002_version_annotation_tasks(process_cpam0002_tasks):
    assert process_cpam0002_tasks['version'].call_count == 7


@pytest.fixture(name="cpam0046_hgvs_variant_json")
def fixture_cpam0046_hgvs_variant(cpam0046_analysis):
    """Returns the HGVS variant within the CPAM0046 analysis."""
    genomic_units = cpam0046_analysis.units_to_annotate()
    unit = {}
    for genomic_unit in genomic_units:
        if genomic_unit["type"] == GenomicUnitType.HGVS_VARIANT:
            unit = genomic_unit

    return unit

@pytest.fixture(name="process_cpam0002_tasks")
def fixture_extract_and_annotate_cpam0002(cpam0002_annotation_queue):
    mock_extract_result = [{
        'data_set': 'mock_datset',
        'data_source': 'mock_source',
        'version': '0.0',
        'value': '9000',
    }]

    with(
        patch("src.core.annotation_task.AnnotationTaskInterface.extract", return_value=mock_extract_result) as extract_task_annotate,
        patch("src.core.annotation_task.VersionAnnotationTask.annotate") as version_task_annotate,
        patch("src.core.annotation_task.ForgeAnnotationTask.annotate") as forge_task_annotate,
        patch("src.core.annotation_task.HttpAnnotationTask.annotate") as http_task_annotate,
        patch("src.core.annotation_task.NoneAnnotationTask.annotate") as none_task_annotate
    ):
        skip_depends = SkipDepedencies()
        mock_genomic_unit_collection = Mock(spec=GenomicUnitCollection)
        mock_genomic_unit_collection.find_genomic_unit_annotation_value.side_effect = skip_depends.skip_hgncid_get_value_first_time_mock
        mock_genomic_unit_collection.annotation_exist.return_value = False

        AnnotationService.process_tasks(cpam0002_annotation_queue, mock_genomic_unit_collection)
        yield {
            'extract': extract_task_annotate,
            'version': version_task_annotate,
            'http': http_task_annotate,
            'none': none_task_annotate,
            'forge': forge_task_annotate,
            'genomic_unit_collection': mock_genomic_unit_collection
        }


class SkipDepedencies:

    def __init__(self, dependencies_to_skip=["HGNC_ID"]):
        self.skip_tracker = {}
        self.to_skip = dependencies_to_skip

    def skip_hgncid_get_value_first_time_mock(self, *args):
        unit, name = args

        should_skip = (name in self.to_skip and name not in self.skip_tracker)
        return self.skip_tracker.setdefault(name, None) if should_skip else f"{unit['unit']}-{name}-value"

@pytest.fixture(name="process_cpam0046_tasks")
def fixture_extract_and_annotate_cpam0046(cpam0046_annotation_queue):
    mock_extract_result = [{
        'data_set': 'mock_datset',
        'data_source': 'mock_source',
        'version': '0.0',
        'value': '9000',
    }]

    with(
        patch("src.core.annotation_task.AnnotationTaskInterface.extract", return_value=mock_extract_result) as extract_task_annotate,
        patch("src.core.annotation_task.VersionAnnotationTask.annotate") as version_task_annotate,
        patch("src.core.annotation_task.ForgeAnnotationTask.annotate") as forge_task_annotate,
        patch("src.core.annotation_task.HttpAnnotationTask.annotate") as http_task_annotate,
        patch("src.core.annotation_task.NoneAnnotationTask.annotate") as none_task_annotate
    ):
        skip_depends = SkipDepedencies()
        mock_genomic_unit_collection = Mock(spec=GenomicUnitCollection)
        mock_genomic_unit_collection.find_genomic_unit_annotation_value.side_effect = skip_depends.skip_hgncid_get_value_first_time_mock
        mock_genomic_unit_collection.annotation_exist.return_value = False

        AnnotationService.process_tasks(cpam0046_annotation_queue, mock_genomic_unit_collection)
        yield {
            'extract': extract_task_annotate,
            'version': version_task_annotate,
            'http': http_task_annotate,
            'none': none_task_annotate,
            'forge': forge_task_annotate,
            'genomic_unit_collection': mock_genomic_unit_collection
        }
