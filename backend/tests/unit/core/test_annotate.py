"""Tests to verify annotation tasks"""

from unittest.mock import AsyncMock, MagicMock, Mock, patch
import pytest

import asyncio
from src.core.annotation import AnnotationService
from src.enums import GenomicUnitType
from src.repository.analysis_collection import AnalysisCollection
from src.repository.genomic_unit_collection import GenomicUnitCollection

from ...test_utils import SkipDependencies

@pytest.mark.anyio
async def test_queuing_annotations_for_genomic_units(cpam0046_analysis, annotation_config_collection):
    """Verifies annotations are queued according to the specific genomic units"""
    annotation_service = AnnotationService(annotation_config_collection)
    mock_queue = Mock()
    await annotation_service.queue_annotation_tasks(cpam0046_analysis, mock_queue)
    assert mock_queue.put.call_count == 9

    actual_queued_genomic_units = [put_call.args[0].genomic_unit['unit'] for put_call in mock_queue.put.call_args_list]

    assert "NM_170707.3:c.745C>T" in actual_queued_genomic_units

@pytest.mark.anyio
async def test_processing_cpam0046_annotation_tasks(process_cpam0046_tasks):
    """Verifies that each item on the annotation queue is read and executed"""
    assert process_cpam0046_tasks['http'].call_count == 6
    assert process_cpam0046_tasks['none'].call_count == 0
    assert process_cpam0046_tasks['forge'].call_count == 2

    assert process_cpam0046_tasks['extract'].call_count == 8

@pytest.mark.anyio
async def test_processing_cpam0002_annotations_tasks(process_cpam0002_tasks):
    """
        Verifies that the annotation collection is being sent the proper amount of extracted annotations for
        CPAM analysis 0002
    """

    assert process_cpam0002_tasks['http'].call_count == 6
    assert process_cpam0002_tasks['none'].call_count == 0
    assert process_cpam0002_tasks['forge'].call_count == 2

    assert process_cpam0002_tasks['extract'].call_count == 8

    process_cpam0002_tasks['genomic_unit_collection'].annotate_genomic_unit.assert_called()

@pytest.mark.anyio
async def test_processing_cpam0002_annotation_tasks_for_datasets_with_dependencies(process_cpam0002_tasks):
    """
    Tests that the dependencies will put the annotation task back onto the processing queue when its missing a
    depedency
    """

    assert process_cpam0002_tasks['genomic_unit_collection'].find_genomic_unit_annotation_value.call_count == 4

async def test_processing_cpam0002_datasets_with_dependencies(cpam0002_annotation_queue, process_cpam0002_tasks):
    """ Confirms that the datasets with dependencies configured to annotate for analysis CPAM0002 are processed """
    assert cpam0002_annotation_queue.empty()

    assert process_cpam0002_tasks['http'].call_count == 6
    assert process_cpam0002_tasks['none'].call_count == 0
    assert process_cpam0002_tasks['forge'].call_count == 2

    assert process_cpam0002_tasks['extract'].call_count == 8

@pytest.mark.anyio
def test_processing_cpam0002_version_annotation_tasks(process_cpam0002_tasks):
    """
    Asserts that each dataset configured to annotate for analysis CPAM0002 calculates the datasets version.
    This includes the datasets' versions are cached after being calculated the first time. There is one unique
    version URL for 4 tasks, rosalution version for 3 tasks, and 2 date tasks, resulting in 3 times the version
    needs to be calculated.
    """
    assert process_cpam0002_tasks['version'].call_count == 3

@pytest.fixture(name="cpam0046_hgvs_variant_json")
def fixture_cpam0046_hgvs_variant(cpam0046_analysis):
    """Returns the HGVS variant within the CPAM0046 analysis."""
    genomic_units = cpam0046_analysis.get_all_units_to_annotate()
    unit = {}
    for genomic_unit in genomic_units:
        if genomic_unit["type"] == GenomicUnitType.HGVS_VARIANT:
            unit = genomic_unit

    return unit

@pytest.fixture(name="process_cpam0002_tasks")
def fixture_extract_and_annotate_cpam0002(cpam0002_annotation_queue, get_dataset_manifest_config, settings, async_mongo_patch):
    """
    Emulates processing the annotations for the configured genomic unit's datasets within the CPAM0002 analysis.
    """
    mock_extract_result = [{
        'data_set': 'mock_datset',
        'data_source': 'mock_source',
        'version': '0.0',
        'value': '9000',
    }]

    with (
        patch("src.core.annotation_task.AnnotationTaskInterface.extract", return_value=mock_extract_result) as extract_task_annotate,
        patch("src.core.annotation_task.AnnotationTaskInterface.extract_version", return_value='fake-version') as extract_task_version_annotate,
        patch("src.core.annotation_task.VersionAnnotationTask.annotate") as version_task_annotate,
        patch("src.core.annotation_task.ForgeAnnotationTask.annotate") as forge_task_annotate,
        patch("src.core.annotation_task.HttpAnnotationTask.annotate") as http_task_annotate,
        patch("src.core.annotation_task.NoneAnnotationTask.annotate") as none_task_annotate
    ):
        skip_depends = SkipDependencies()

        repositories = async_mongo_patch['repositories']
        mock_genomic_unit_collection = repositories["genomic_unit"]
        mock_analysis_collection = repositories["analysis"]
        mock_genomic_unit_collection.find_genomic_unit_annotation_value.side_effect = (
            skip_depends.skip_find_genomic_unit_annotation_value_mock
        )
        mock_analysis_collection.get_manifest_dataset_config.return_value = get_dataset_manifest_config(
            "CPAM0002", "VMA21", 'HGNC_ID'
        )
        mock_genomic_unit_collection.annotation_exist.return_value = False

        AnnotationService.process_tasks( cpam0002_annotation_queue, settings )

        yield {
            'extract': extract_task_annotate, 'version': version_task_annotate, 'http': http_task_annotate,
            'none': none_task_annotate, 'forge': forge_task_annotate,
            'genomic_unit_collection': mock_genomic_unit_collection, 'extract_version': extract_task_version_annotate
        }

@pytest.fixture(name="process_cpam0046_tasks")
def fixture_extract_and_annotate_cpam0046(cpam0046_annotation_queue, get_dataset_manifest_config, settings, async_mongo_patch):
    """
    Emulates processing the annotations for the configured genomic unit's datasets within the CPAM0046 analysis.
    """
    mock_extract_result = [{
        'data_set': 'mock_datset',
        'data_source': 'mock_source',
        'version': '0.0',
        'value': '9000',
    }]

    with (
        patch("src.core.annotation_task.AnnotationTaskInterface.extract", return_value=mock_extract_result) as extract_task_annotate,
        patch("src.core.annotation_task.AnnotationTaskInterface.extract_version", return_value='fake-version') as extract_task_version_annotate,
        patch("src.core.annotation_task.VersionAnnotationTask.annotate") as version_task_annotate,
        patch("src.core.annotation_task.ForgeAnnotationTask.annotate") as forge_task_annotate,
        patch("src.core.annotation_task.HttpAnnotationTask.annotate") as http_task_annotate,
        patch("src.core.annotation_task.NoneAnnotationTask.annotate") as none_task_annotate
    ):
        skip_depends_find_annotation_value = SkipDependencies()

        dependency_dataset = get_dataset_manifest_config("CPAM0046", "LMNA", 'HGNC_ID')
        skip_depends_get_manifest_dataset_config = SkipDependencies()
        skip_depends_get_manifest_dataset_config.set_analysis_manifest_entry(dependency_dataset)

        repositories = async_mongo_patch['repositories']
        repositories["genomic_unit"].find_genomic_unit_annotation_value.side_effect = (
            skip_depends_find_annotation_value.skip_find_genomic_unit_annotation_value_mock
        )
        repositories["analysis"].get_manifest_dataset_config.side_effect = (
            skip_depends_get_manifest_dataset_config.skip_get_manifest_entry_analysis
        )
        repositories["genomic_unit"].annotation_exist.return_value = False

        AnnotationService.process_tasks(cpam0046_annotation_queue, settings)
        yield {
            'extract': extract_task_annotate, 'version': version_task_annotate, 'http': http_task_annotate,
            'none': none_task_annotate, 'forge': forge_task_annotate,
            'genomic_unit_collection': repositories["genomic_unit"], 'extract_version': extract_task_version_annotate
        }

@pytest.fixture(name="async_mongo_patch")
def fixture_mongo_client():
    """Patching the AsyncMongoClient and AsyncGridfs since encapsulated in event loop."""
    with (
        patch("src.core.annotation.AsyncMongoClient") as mock_client_class,
        patch("src.core.annotation.AsyncGridFS") as mock_gridfs_class,
        patch("src.core.annotation.Database") as mock_database_class,
        patch("src.database.Database") as mock_database_class_try_again
    ):

        mock_client_instance = MagicMock()
        mock_client_class.return_value.__aenter__ = AsyncMock(return_value=mock_client_instance)
        mock_client_class.return_value.__aexit__ = AsyncMock(return_value=None)

        mock_gridfs_instance = MagicMock()
        mock_gridfs_class.return_value = mock_gridfs_instance

        mock_database_instance = MagicMock()
        mock_repositories = {
            "genomic_unit": AsyncMock(spec=GenomicUnitCollection),
            "analysis": AsyncMock(spec=AnalysisCollection)
        }

        mock_database_instance.return_value = mock_repositories
        mock_database_class.return_value = mock_database_instance

        mock_database_class_try_again.return_value = mock_database_instance

        # Yield a dictionary or a custom object so your test can access individual mocks if needed
        yield {
            "client_cls": mock_client_class,
            "client_instance": mock_client_instance,
            "gridfs_instance": mock_gridfs_instance,
            "repositories": mock_repositories,
            "database": mock_database_class_try_again,
        }
