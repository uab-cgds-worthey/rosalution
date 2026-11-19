"""Project Routes Integration test"""

import asyncio
import json

from unittest.mock import MagicMock, patch
import pytest

from fastapi import BackgroundTasks
from fastapi.testclient import TestClient

from src.core.annotation import AnnotationService
from src.core.annotation_task import AnnotationTaskInterface, ForgeAnnotationTask, \
    HttpAnnotationTask, NoneAnnotationTask, VersionAnnotationTask

from ..test_utils import assets_fixture_filepath, read_test_fixture


@pytest.fixture
def captured_tasks(monkeypatch):
    """Fixture which monkey patches the FastAPI BackgroundTasks method in order to manually control its execution"""
    tasks = []

    def mock_add_task(method, *args, **kwargs):
        tasks.append((method, args, kwargs))

    monkeypatch.setattr(BackgroundTasks, "add_task", mock_add_task)
    return tasks


@pytest.mark.anyio
@pytest.mark.usefixtures(
    "captured_tasks", "disable_info_logging", "mock_annotation_requests",
    "mock_security_get_create_project_authorization"
)
async def test_annotation_processing_for_new_analysis(
    client: TestClient, mock_access_token, live_annotation_queue, mock_repositories
):
    """ Testing if the create analysis function works with file upload """

    analysis_import_json_filepath = assets_fixture_filepath('cpam0046-new-import.json')
    with (
        patch(
            'src.core.annotation_task.AnnotationTaskInterface.extract',
            wraps=AnnotationTaskInterface.extract,
            autospec=True
        ) as extract_task_annotate,
        patch(
            'src.core.annotation_task.AnnotationTaskInterface.extract_version',
            wraps=AnnotationTaskInterface.extract_version,
            autospec=True
        ) as extract_task_version_annotate,
        patch(
            'src.core.annotation_task.VersionAnnotationTask.annotate',
            wraps=VersionAnnotationTask.annotate,
            autospec=True
        ),
        patch(
            'src.core.annotation_task.ForgeAnnotationTask.annotate', wraps=ForgeAnnotationTask.annotate, autospec=True
        ) as forge_task_annotate,
        patch('src.core.annotation_task.HttpAnnotationTask.annotate', wraps=HttpAnnotationTask.annotate,
              autospec=True) as http_task_annotate,
        patch('src.core.annotation_task.NoneAnnotationTask.annotate', wraps=NoneAnnotationTask.annotate, autospec=True)
        as none_task_annotate, open(analysis_import_json_filepath, "rb") as import_file
    ):
        response = await client.post(
            "/project/695d5b157709ebcd1c7325c1/analysis",
            headers={"Authorization": "Bearer " + mock_access_token},
            files={"phenotips_file": ("cpam0046-new-import.json", import_file.read())}
        )

        assert live_annotation_queue.annotation_queue.qsize() == 10

        running_event_loop = asyncio.get_running_loop()

        # Running protected method to avoid running the run process tasks in a new event loop with the main run method
        # pylint: disable=protected-access
        await AnnotationService._run_process_tasks(running_event_loop, live_annotation_queue, mock_repositories)
        assert live_annotation_queue.annotation_queue.qsize() == 0

        assert http_task_annotate.call_count == 2
        assert none_task_annotate.call_count == 0
        assert forge_task_annotate.call_count == 8

        assert extract_task_annotate.call_count == 10
        assert extract_task_version_annotate.call_count == 3

    assert response.status_code == 200
    response_data = json.loads(response.text)
    assert response_data['latest_status'] == "Preparation"
    assert response_data['timeline'][0]['username'] == '3bghhsmnyqi6uxovazy07ryn9q1tqbnt'


@pytest.fixture(name="mock_annotation_requests")
def fixture_mock_requests_api(cpamn0046_requests_responses):
    """ Fixture that mocks several REST API responses from several annotation sources """

    def get_response(url):
        if url not in cpamn0046_requests_responses:
            print(f"ERROR - Missing Response for URL: {url}")
            return {}
        return cpamn0046_requests_responses[url]

    # No need to operate or do any with the other requests api arguments when mocking
    # pylint: disable=unused-argument
    def mock_get_method(url, verify, headers, timeout):
        mock_get_response = MagicMock()
        mock_get_response.json.return_value = get_response(url)
        return mock_get_response

    with patch('src.core.annotation_task.requests') as mock_requests:

        mock_requests.get.side_effect = mock_get_method

        yield mock_requests


@pytest.fixture(name="cpamn0046_requests_responses")
def fixture_cpam0046_responses_from_annotations_http_requests():
    """HTTP Responses for CPAM0046 analyis"""
    return read_test_fixture("cpam0046-requests-responses.json")
