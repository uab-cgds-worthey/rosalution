"""Tests to verify annotation tasks"""

import logging
from unittest.mock import AsyncMock, MagicMock, patch
import pytest

from src.enums import GenomicUnitType
from src.core.annotation_task import AnnotationTaskFactory
from src.core.annotation import AnnotationProcess, AnnotationQueue, AnnotationService

logger = logging.getLogger(__name__)


@pytest.mark.anyio
async def test_queuing_annotations_for_genomic_units(cpam0046_analysis, annotation_config_collection):
    """Verifies annotations are queued according to the specific genomic units"""
    annotation_service = AnnotationService(annotation_config_collection)
    mock_queue = MagicMock()
    await annotation_service.queue_annotation_tasks(cpam0046_analysis, mock_queue)
    assert mock_queue.put.call_count == 9

    actual_queued_genomic_units = [put_call.args[0].genomic_unit['unit'] for put_call in mock_queue.put.call_args_list]

    assert "NM_170707.3:c.745C>T" in actual_queued_genomic_units


@pytest.mark.anyio
async def test_queuing_annotations_for_genomic_units_by_unit(cpam0046_analysis, annotation_config_collection):
    """Verifies annotations are queued according to the specific genomic units"""
    units_to_annotate = [{
        'unit': 'NM_170707.3:c.745C>T', 'type': GenomicUnitType.HGVS_VARIANT, 'transcript': 'NM_170707',
        'protein': 'p.Arg249Trp'
    }]

    annotation_service = AnnotationService(annotation_config_collection)
    mock_queue = MagicMock()
    await annotation_service.queue_annotation_tasks_by_unit(cpam0046_analysis, units_to_annotate, mock_queue)
    assert mock_queue.put.call_count == 3

    actual_queued_genomic_units = [put_call.args[0].genomic_unit['unit'] for put_call in mock_queue.put.call_args_list]

    assert "NM_170707.3:c.745C>T" in actual_queued_genomic_units


def test_annotation_process_queue_tasks_in_tasks_worker(http_annotation_task_gene, annotation_processer):
    """Asserts the processor has tasks processing when a task is queued to the event loop"""
    assert annotation_processer.are_tasks_processing() is False
    annotation_processer.queue_task_in_tasks_worker(http_annotation_task_gene)
    assert annotation_processer.are_tasks_processing() is True


def test_handle_annotation_unit_version_calculation_not_cached(
    gene_hpo_annotation_unit, annotation_processer, mock_event_loop
):
    """Asserts the annotation process will create an annotation version task and add to even loop"""
    annotation_processer.handle_annotation_unit_version_calcuation(gene_hpo_annotation_unit)
    assert mock_event_loop.create_task.call_count == 1


@pytest.mark.usefixtures('mock_event_loop')
def test_handle_annotation_unit_version_calculation_cache_setup(gene_hpo_annotation_unit, annotation_processer):
    """Asserts the annotation process handles provisioning the annotation unit version cache """
    version_task = AnnotationTaskFactory.create_version_task(gene_hpo_annotation_unit)
    cache_id = version_task.get_version_cache_id()
    assert annotation_processer.is_version_cache_setup(cache_id) is False
    annotation_processer.handle_annotation_unit_version_calcuation(gene_hpo_annotation_unit)
    assert annotation_processer.is_version_cache_setup(cache_id) is True


@pytest.mark.usefixtures('mock_event_loop')
def test_handle_annotation_unit_version_calculation_set_via_cache(
    gene_hpo_annotation_unit, annotation_processer, mock_queue
):
    """Asserts the annotation process handles provisioning the annotation unit version cache """

    version_task = AnnotationTaskFactory.create_version_task(gene_hpo_annotation_unit)
    cache_id = version_task.get_version_cache_id()

    # sets up the annotation version cache
    annotation_processer.handle_annotation_unit_version_calcuation(gene_hpo_annotation_unit)
    assert annotation_processer.is_version_cache_setup(cache_id) is True

    annotation_processer.set_version_in_cache(cache_id, version_task.annotate())

    annotation_processer.handle_annotation_unit_version_calcuation(gene_hpo_annotation_unit)
    assert mock_queue.put.call_count == 1


@pytest.mark.anyio
async def test_process_annotation_task_to_completion(
    hpo_annotation_response, http_annotation_task_gene, mock_annotation_task_worker, annotation_processer
):
    """Asserts the annotation process cleans up tasks after completion """

    mock_annotation_task_worker.result.return_value = hpo_annotation_response

    assert annotation_processer.are_tasks_processing() is False
    annotation_processer.queue_task_in_tasks_worker(http_annotation_task_gene)
    assert annotation_processer.are_tasks_processing() is True
    assert mock_annotation_task_worker.add_done_callback.call_count == 1

    await annotation_processer.on_task_complete(mock_annotation_task_worker)

    assert annotation_processer.are_tasks_processing() is False


@pytest.mark.anyio
async def test_process_annotation_version_task_to_completion(
    get_version_task, mock_annotation_task_worker, annotation_processer
):
    """Asserts the annotation processes results of annotation version tasks """

    omic_unit, dataset = ('VMA21', 'Entrez Gene Id')
    version_task = get_version_task(omic_unit, dataset)
    mock_annotation_task_worker.result.return_value = {"rosalution": "rosalution-manifest-00"}

    assert annotation_processer.are_tasks_processing() is False
    annotation_processer.queue_task_in_tasks_worker(version_task)
    assert annotation_processer.are_tasks_processing() is True
    assert mock_annotation_task_worker.add_done_callback.call_count == 1

    await annotation_processer.on_task_complete(mock_annotation_task_worker)
    assert annotation_processer.are_tasks_processing() is False


@pytest.mark.anyio
@pytest.mark.parametrize(
    "omic_unit_dataset", [(('VMA21', "Entrez Gene Id")), (('NM_001017980.3:c.164G>T', "Polyphen Prediction"))]
)
async def test_handle_annotation_unit_dependency_exist(
    omic_unit_dataset, get_annotation_unit, get_dataset_manifest_config, analysis_collection, genomic_unit_collection,
    annotation_processer
):
    """Asserts the annotation processes handles dependencies, including transcripts for variants """
    omic_unit, dataset = omic_unit_dataset
    annotation_unit = get_annotation_unit(omic_unit, dataset)
    analysis_dataset_config = get_dataset_manifest_config('CPAM0002', omic_unit, dataset)
    analysis_collection.get_manifest_dataset_config = AsyncMock(return_value=analysis_dataset_config)
    genomic_unit_collection.analysis_dataset_config = AsyncMock(return_value="test-value-returnedd")
    assert len(annotation_unit.get_missing_dependencies()) == 1
    await annotation_processer.handle_annotation_unit_dependencies(annotation_unit)
    assert len(annotation_unit.get_missing_dependencies()) == 0


@pytest.mark.anyio
async def test_handle_annotation_unit_dependency_missing(
    get_annotation_unit, analysis_collection, annotation_processer
):
    """Asserts the annotation processes handles dependencies if they are missing """

    omic_unit, dataset = ('VMA21', 'Entrez Gene Id')
    annotation_unit = get_annotation_unit(omic_unit, dataset)
    analysis_collection.get_manifest_dataset_config = AsyncMock(return_value=None)
    assert len(annotation_unit.get_missing_dependencies()) == 1
    await annotation_processer.handle_annotation_unit_dependencies(annotation_unit)
    assert len(annotation_unit.get_missing_dependencies()) == 1


@pytest.mark.anyio
@pytest.mark.parametrize(
    "exception_type,error_message", [
        (TypeError, "Invalid type occured in annotation"),
        (FileNotFoundError, "Missing file to query annotation"),
        (RuntimeError, "Failed to extract annotation result"),
    ]
)
async def test_log_annotation_exception_failures(
    exception_type, error_message, http_annotation_task_gene, mock_annotation_task_worker, annotation_processer
):
    """Asserts the annotation processes task results catch and log exception failures"""

    with patch('src.core.annotation.logger') as error_logger_spy:
        mock_annotation_task_worker.result.side_effect = exception_type(error_message)

        assert annotation_processer.are_tasks_processing() is False
        annotation_processer.queue_task_in_tasks_worker(http_annotation_task_gene)
        assert annotation_processer.are_tasks_processing() is True
        assert mock_annotation_task_worker.add_done_callback.call_count == 1

        await annotation_processer.on_task_complete(mock_annotation_task_worker)
        assert error_logger_spy.error.call_count == 1

        positional_args = error_logger_spy.error.call_args_list[0].args
        actual_error_log = " ".join(str(arg) for arg in positional_args)
        assert error_message in actual_error_log


@pytest.mark.anyio
async def test_track_annotation_exception_failures_to_report(
    http_annotation_task_gene, mock_annotation_task_worker, annotation_processer
):
    """Asserts the annotation processes task results track exception failures"""

    error_message = "Invalid type occured in annotation"
    with patch('src.core.annotation.logger') as error_logger_spy:
        mock_annotation_task_worker.result.side_effect = TypeError(error_message)

        assert annotation_processer.are_tasks_processing() is False
        annotation_processer.queue_task_in_tasks_worker(http_annotation_task_gene)
        assert annotation_processer.are_tasks_processing() is True
        assert mock_annotation_task_worker.add_done_callback.call_count == 1

        await annotation_processer.on_task_complete(mock_annotation_task_worker)
        annotation_processer.log_dataset_failures()
        assert error_logger_spy.error.call_count == 3


@pytest.fixture(name="mock_queue")
def fixture_annotation_queue_mock():
    """Fixture that mocks the AnnotationQueue"""
    annotation_queue = AnnotationQueue()
    spy_wrapper = MagicMock(annotation_queue)
    return spy_wrapper


@pytest.fixture(name="annotation_processer")
def fixture_annotation_process(mock_queue, mock_event_loop, genomic_unit_collection, analysis_collection):
    """Fixture that provisions the AnnotationProcess with a mock event loop, and mock queue"""
    processor = AnnotationProcess(mock_queue, genomic_unit_collection, analysis_collection)
    processor.set_tasks_executor(mock_event_loop)
    return processor


@pytest.fixture(name="mock_annotation_task_worker")
def fixture_annotation_task_worker():
    """Fixture that provisions the an asyncio task work"""
    mock_annotation_task_worker = MagicMock()
    mock_annotation_task_worker.add_done_callback = MagicMock()
    return mock_annotation_task_worker


@pytest.fixture(name="mock_event_loop")
def fixture_mock_event_loop(mock_annotation_task_worker):
    """Fixture that emulates an event loop that creates asyncio tasks"""

    def mock_create_task(coroutine_method):
        """Fixture method that emulates an creating an asyncio task. It must result the coroutine provided"""
        coroutine_method.close()
        return mock_annotation_task_worker

    mock_event_loop = MagicMock()
    mock_event_loop.create_task = MagicMock(side_effect=mock_create_task)

    def execute_passed_function(mock_annotation_method, *args, **kwargs):
        """Fixture method that executes the provided method to run in a task"""
        return mock_annotation_method(*args, **kwargs)

    with (patch("src.core.annotation.asyncio.to_thread", new_callable=AsyncMock) as mock_to_thread,):
        mock_to_thread.side_effect = execute_passed_function

        yield mock_event_loop
