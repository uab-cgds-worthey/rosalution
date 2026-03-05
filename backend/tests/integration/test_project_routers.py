"""Project Routes Integration test"""

import json

from unittest.mock import patch
import pytest

from fastapi import BackgroundTasks

from src.core.annotation import AnnotationService

from ..test_utils import fixture_filepath


@pytest.mark.usefixtures("mock_security_get_create_project_authorization")
def test_import_with_new_analysis_json(
    client, mock_access_token, mock_repositories, mock_annotation_queue, annotations_config_collection_json,
    genomic_units_collection_json
):
    """ Testing if the create analysis function works with file upload """
    mock_repositories["analysis"].collection.insert_one.return_value = True
    mock_repositories["analysis"].collection.find_one.return_value = None
    mock_repositories["genomic_unit"].collection.find_one.return_value = None
    mock_repositories['annotation_config'].collection.find.return_value = annotations_config_collection_json
    mock_repositories['genomic_unit'].collection.find.return_value = genomic_units_collection_json

    with patch.object(BackgroundTasks, "add_task", return_value=None) as mock_background_add_task:
        analysis_import_json_filepath = fixture_filepath('new-analysis-import.json')
        with open(analysis_import_json_filepath, "rb") as import_file:
            response = client.post(
                "/project/695d5b157709ebcd1c7325c1/analysis",
                headers={"Authorization": "Bearer " + mock_access_token},
                files={"phenotips_file": ("new-analysis-import.json", import_file.read())}
            )

            import_file.close()

            assert mock_annotation_queue.put.call_count == 9

            mock_background_add_task.assert_called_once_with(
                AnnotationService.process_tasks, mock_annotation_queue, mock_repositories['genomic_unit'],
                mock_repositories['analysis']
            )

    assert response.status_code == 200
    response_data = json.loads(response.text)
    assert response_data['latest_status'] == "Preparation"
    assert response_data['timeline'][0]['username'] == 'johndoe-client-id'
