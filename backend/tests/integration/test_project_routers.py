"""Project Routes Integration test"""

import json

from unittest.mock import patch
import pytest

from fastapi import BackgroundTasks
from fastapi.testclient import TestClient

from src.core.annotation import AnnotationService

from ..test_utils import assets_fixture_filepath


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories", "mock_security_get_create_project_authorization")
async def test_import_with_new_analysis_json(
    client: TestClient, mock_access_token, mock_annotation_queue, mock_settings
):
    """ Testing if the create analysis function works with file upload """
    with patch.object(BackgroundTasks, "add_task", return_value=None) as mock_background_add_task:
        analysis_import_json_filepath = assets_fixture_filepath('new-analysis-import.json')
        with open(analysis_import_json_filepath, "rb") as import_file:
            response = await client.post(
                "/project/695d5b157709ebcd1c7325c1/analysis",
                headers={"Authorization": "Bearer " + mock_access_token},
                files={"phenotips_file": ("new-analysis-import.json", import_file.read())}
            )

            import_file.close()

            assert mock_annotation_queue.put.call_count == 9

            mock_background_add_task.assert_called_once_with(
                AnnotationService.process_tasks, mock_annotation_queue, mock_settings
            )

    assert response.status_code == 200
    response_data = json.loads(response.text)
    assert response_data['latest_status'] == "Preparation"
    assert response_data['timeline'][0]['username'] == '3bghhsmnyqi6uxovazy07ryn9q1tqbnt'
