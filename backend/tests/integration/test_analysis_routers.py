"""Analysis Routes Integration test"""

import json
import datetime

from unittest.mock import patch

import pytest
from fastapi import BackgroundTasks
from src.enums import ThirdPartyLinkType
from src.core.annotation import AnnotationService

from ..test_utils import fixture_filepath, read_test_fixture


def test_get_analyses(client, mock_access_token, mock_repositories, analysis_collection_json):
    """Testing that the correct number of analyses were returned and in the right order"""
    mock_repositories['analysis'].collection.find.return_value = analysis_collection_json

    response = client.get("/analysis", headers={"Authorization": "Bearer " + mock_access_token})

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[1]["name"] == "CPAM0047"


def test_get_analysis_summary(client, mock_access_token, mock_repositories, analysis_collection_json):
    """Testing if the analysis summary endpoint returns all of the analyses available"""
    mock_repositories['analysis'].collection.find.return_value = analysis_collection_json
    response = client.get("/analysis/summary", headers={"Authorization": "Bearer " + mock_access_token})
    assert len(response.json()) == 2


def test_get_summary_by_name(client, mock_access_token, mock_repositories, cpam0002_analysis_json):
    """Tests the summary_by_name endpoint"""
    mock_repositories['analysis'].collection.find_one.return_value = cpam0002_analysis_json
    response = client.get("/analysis/CPAM0002/summary", headers={"Authorization": "Bearer " + mock_access_token})

    assert response.status_code == 200
    assert response.json()["name"] == "CPAM0002"


def test_import_analysis_with_phenotips_json( # pylint: disable=too-many-arguments
    client,
    mock_access_token,
    mock_repositories,
    mock_annotation_queue,
    annotations_config_collection_json,
    genomic_units_collection_json,
    mock_security_get_current_user,  # pylint: disable=unused-argument
):
    """ Testing if the create analysis function works with file upload """
    mock_repositories["analysis"].collection.insert_one.return_value = True
    mock_repositories["analysis"].collection.find_one.return_value = None
    mock_repositories["genomic_unit"].collection.find_one.return_value = None
    mock_repositories['annotation_config'].collection.find.return_value = annotations_config_collection_json
    mock_repositories['genomic_unit'].collection.find.return_value = genomic_units_collection_json

    with patch.object(BackgroundTasks, "add_task", return_value=None) as mock_background_add_task:
        analysis_import_json_filepath = fixture_filepath('phenotips-import.json')
        with open(analysis_import_json_filepath, "rb") as phenotips_file:
            response = client.post(
                "/analysis",
                headers={"Authorization": "Bearer " + mock_access_token},
                files={"phenotips_file": ("phenotips-import.json", phenotips_file.read())}
            )

            phenotips_file.close()

            assert mock_annotation_queue.put.call_count == 49

            mock_background_add_task.assert_called_once_with(
                AnnotationService.process_tasks, mock_annotation_queue, mock_repositories['genomic_unit']
            )

    assert response.status_code == 200
    response_data = json.loads(response.text)
    assert response_data['latest_status'] == "Preparation"
    assert response_data['timeline'][0]['username'] == 'johndoe-client-id'


def test_get_genomic_units_success(client, mock_access_token, mock_repositories, cpam0002_analysis_json):
    """ Testing the get genomic units endpoint """
    mock_repositories["analysis"].collection.find_one.return_value = cpam0002_analysis_json

    response = client.get("/analysis/CPAM0002/genomic_units", headers={"Authorization": "Bearer " + mock_access_token})

    expected_genomic_unit_response = {
        "genes": {"VMA21": ["NM_001017980.3:c.164G>T(p.Gly55Val)"]},
        "variants": ["NM_001017980.3:c.164G>T(p.Gly55Val)"]
    }

    assert response.status_code == 200
    assert response.json() == expected_genomic_unit_response


def test_get_genomic_units_analysis_does_not_exist(client, mock_access_token, mock_repositories):
    """ Testing the get genomic units endpoint """
    mock_repositories["analysis"].collection.find_one.return_value = None

    response = client.get("/analysis/CPAM0002/genomic_units", headers={"Authorization": "Bearer " + mock_access_token})

    assert response.status_code == 404


def test_get_genomic_units_does_not_exist(client, mock_access_token, mock_repositories, cpam0002_analysis_json):
    """ Testing the get genomic units endpoint """
    mock_repositories["analysis"].collection.find_one.return_value = cpam0002_analysis_json.pop("genomic_units")

    response = client.get("/analysis/CPAM0002/genomic_units", headers={"Authorization": "Bearer " + mock_access_token})

    assert response.status_code == 404


def test_attach_third_party_link(client, mock_access_token, mock_repositories, cpam0002_analysis_json):
    """ Testing the attach third party link endpoint """
    mock_repositories["analysis"].collection.find_one.return_value = cpam0002_analysis_json
    mock_repositories["analysis"].collection.find_one_and_update.return_value = {
        "_id": 'valid-response-not-real-return'
    }
    response = client.put(
        "/analysis/CPAM0002/attach/monday_com",
        headers={"Authorization": "Bearer " + mock_access_token},
        data={"link": "https://monday.com"}
    )

    assert response.status_code == 200

    save_call_args = mock_repositories["analysis"].collection.find_one_and_update.call_args[0]
    (actual_name, actual_update_query) = save_call_args
    assert actual_name['name'] == "CPAM0002"

    assert actual_update_query['$push']['third_party_links'] == {
        "type": ThirdPartyLinkType.MONDAY_COM, "link": "https://monday.com"
    }


def test_attach_third_party_link_analysis_does_not_exist(client, mock_access_token, mock_repositories):
    """ Testing the attach third party link endpoint """
    mock_repositories["analysis"].collection.find_one.return_value = None
    response = client.put(
        "/analysis/CPAM0002/attach/monday_com",
        headers={"Authorization": "Bearer " + mock_access_token},
        data={"link": "monday.com"}
    )

    assert response.status_code == 409


def test_attach_third_party_link_invalid_enum(client, mock_access_token, mock_repositories, cpam0002_analysis_json):
    """ Testing the attach third party link endpoint """
    mock_repositories["analysis"].collection.find_one.return_value = cpam0002_analysis_json
    response = client.put(
        "/analysis/CPAM0002/attach/BAD_ENUM",
        headers={"Authorization": "Bearer " + mock_access_token},
        data={"link": "monday.com"}
    )

    assert response.status_code == 422


def test_mark_ready(client, mock_access_token, mock_repositories, cpam0002_analysis_json):
    """ Testing the update analysis event endpoint """
    staging_analysis_timeline = cpam0002_analysis_json
    staging_analysis_timeline["timeline"] = [{
        'event': 'create',
        'timestamp': datetime.datetime(2022, 11, 10, 16, 52, 43, 910000),
        'username': 'johndoe',
    }]
    mock_repositories["analysis"].collection.find_one.return_value = staging_analysis_timeline

    expected = read_test_fixture("analysis-CPAM0002.json")
    expected["timeline"] = [
        {
            'event': 'create',
            'timestamp': '2022-11-10T16:52:43.910000',
            'username': 'johndoe',
        },
        {
            'event': 'ready',
            'timestamp': '2022-11-10T16:52:52.301003',
            'username': 'johndoe',
        },
    ]

    mock_repositories["analysis"].collection.find_one_and_update.return_value = expected

    response = client.put("/analysis/CPAM0002/event/ready", headers={"Authorization": "Bearer " + mock_access_token})

    assert response.status_code == 200


def test_mark_ready_analysis_does_not_exist(client, mock_access_token, mock_repositories):
    """ Testing the mark ready endpoint """
    mock_repositories["analysis"].collection.find_one.return_value = None

    response = client.put("/analysis/CPAM2222/event/ready", headers={"Authorization": "Bearer " + mock_access_token})

    assert response.status_code == 409
    assert response.json() == {'detail': 'Analysis with name CPAM2222 does not exist.'}


@pytest.fixture(name="exported_phenotips_to_import_json")
def fixture_phenotips_import():
    """Returns a phenotips json fixture"""
    return read_test_fixture("phenotips-import.json")
