"""Analysis Routes Integration test"""

import json
import os
from unittest.mock import patch, Mock

import pytest
from fastapi import BackgroundTasks

from bson import ObjectId

from src.core.annotation import AnnotationService

from ..test_utils import read_database_fixture, read_test_fixture


def test_get_analyses(client, mock_access_token, mock_repositories):
    """Testing that the correct number of analyses were returned and in the right order"""
    mock_repositories['analysis'].collection.find.return_value = read_database_fixture(
        "analyses.json")

    response = client.get(
        "/analysis/", headers={"Authorization": "Bearer " + mock_access_token})

    assert response.status_code == 200
    assert len(response.json()) == 5
    assert response.json()[2]["name"] == "CPAM0047"


def test_get_analyses_unauthorized(client, mock_repositories):
    """Tries to get the analyses from the endpoint, but is unauthorized. Does not provide valid token"""
    mock_repositories['analysis'].collection.find.return_value = read_database_fixture(
        "analyses.json")
    response = client.get("/analysis/")

    # This is temporarily changed as security is removed for the analysis endpoints to make development easier
    # assert response.status_code == 401
    assert response.status_code == 200


def test_get_analysis_summary(client, mock_access_token, mock_repositories):
    """Testing if the analysis summary endpoint returns all of the analyses available"""
    mock_repositories['analysis'].collection.find.return_value = read_test_fixture(
        "analyses-summary-db-query-result.json")
    response = client.get(
        "/analysis/summary", headers={"Authorization": "Bearer " + mock_access_token})
    assert len(response.json()) == 5


def test_create_analysis(
    client,
    mock_access_token,
    mock_repositories,
    exported_phenotips_to_import_json,
    mock_annotation_queue
):
    """Testing if the create analysis endpoint creates a new analysis"""
    mock_repositories["analysis"].collection.insert_one.return_value = True
    mock_repositories["analysis"].collection.find_one.return_value = None
    mock_repositories["genomic_unit"].collection.find_one.return_value = None
    mock_repositories['genomic_unit'].collection.find.return_value = read_database_fixture(
        "genomic-units.json")
    mock_repositories['annotation_config'].collection.find.return_value = read_database_fixture(
        "annotations-config.json")

    with patch.object(BackgroundTasks, "add_task", return_value=None) as mock_background_add_task:
        response = client.post(
            "/analysis/import",
            headers={"Authorization": "Bearer " + mock_access_token,
                     "Content-Type": "application/json"},
            json=exported_phenotips_to_import_json,
        )

        assert mock_annotation_queue.put.call_count == 28

        mock_background_add_task.assert_called_once_with(
            AnnotationService.process_tasks,
            mock_annotation_queue,
            mock_repositories['genomic_unit']
        )

    assert response.status_code == 200


def test_create_analysis_with_file(client, mock_access_token, mock_repositories, mock_annotation_queue):
    """ Testing if the create analysis function works with file upload """
    mock_repositories["analysis"].collection.insert_one.return_value = True
    mock_repositories["analysis"].collection.find_one.return_value = None
    mock_repositories["genomic_unit"].collection.find_one.return_value = None
    mock_repositories['annotation_config'].collection.find.return_value = read_database_fixture(
        "annotations-config.json")
    mock_repositories['genomic_unit'].collection.find.return_value = read_database_fixture(
        "genomic-units.json")

    # This is used here because the 'read_fixture' returns a json dict rather than raw binary
    # We actually want to send a binary file through the endpoint to simulate a file being sent
    # then json.loads is used on the other end in the repository.
    # This'll get updated and broken out in the test_utils in the future
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    path_to_file = os.path.join(
        current_directory, '../fixtures/' + 'phenotips-import.json')

    with patch.object(BackgroundTasks, "add_task", return_value=None) as mock_background_add_task:
        with open(path_to_file, "rb") as phenotips_file:
            response = client.post(
                "/analysis/import_file",
                headers={"Authorization": "Bearer " + mock_access_token},
                files={"phenotips_file": (
                    "phenotips-import.json", phenotips_file.read())}
            )

            phenotips_file.close()

            assert mock_annotation_queue.put.call_count == 28

            mock_background_add_task.assert_called_once_with(
                AnnotationService.process_tasks,
                mock_annotation_queue,
                mock_repositories['genomic_unit']
            )

    assert response.status_code == 200


def test_update_analysis(client, mock_access_token, mock_repositories, analysis_updates_json):
    """Testing if the update analysis endpoint updates an existing analysis"""
    mock_repositories["analysis"].collection.find_one_and_update.return_value = analysis_updates_json
    response = client.put(
        "/analysis/update/CPAM0112",
        headers={"Authorization": "Bearer " + mock_access_token,
                 "Content-Type": "application/json"},
        # this is the new analysis data
        json=analysis_updates_json,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "CPAM0112"
    assert response.json()["nominated_by"] == "Dr. Person One"


def test_update_analysis_section(client, mock_access_token, mock_repositories, update_analysis_section_dict,
                                 update_analysis_section_response_json):
    """Testing if the update analysis endpoint updates an existing analysis"""
    mock_repositories["analysis"].collection.find_one_and_update.return_value = update_analysis_section_response_json
    response = client.put(
        "/analysis/update/CPAM0047?section_header=Brief&field_name=Reason",
        headers={"Authorization": "Bearer " + mock_access_token,
                 "Content-Type": "application/json"},
        # this is the new analysis data
        json=update_analysis_section_dict,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "CPAM0047"
    assert response.json()[
        "sections"][0]["content"][1]["value"] == ["the quick brown fox jumps over the lazy dog."]


def test_upload_file_to_analysis(client, mock_access_token, mock_file_upload, mock_repositories):
    """Testing if the upload file endpoint uploads a file to an analysis"""
    # This test currently writes a file to the backend folder, This will eventually be changed to write
    # the mongo database instead with GridFS. We are currently git-ignoring this file to avoid it being commited.
    mock_repositories["analysis"].collection.find_one_and_update.return_value = {
        'fakevalue': 'fakeyfake'}
    mock_repositories["bucket"].bucket.exists.return_value = False
    response = client.post(
        "/analysis/upload/CPAM0002",
        headers={"Authorization": "Bearer " + mock_access_token},
        data=({"comments": "This is a test comment for file test.txt"}),
        files=mock_file_upload
    )
    assert response.status_code == 200


def test_upload_file_already_exists_to_analysis(client, mock_access_token, mock_file_upload, mock_repositories):
    """Testing if the upload file endpoint uploads a file to an analysis"""
    # This test currently writes a file to the backend folder, This will eventually be changed to write
    # the mongo database instead with GridFS. We are currently git-ignoring this file to avoid it being commited.
    mock_repositories["analysis"].collection.find_one_and_update.return_value = {
        'fakevalue': 'fakeyfake'}
    mock_repositories["bucket"].bucket.exists.return_value = True
    response = client.post(
        "/analysis/upload/CPAM0002",
        headers={"Authorization": "Bearer " + mock_access_token},
        data=({"comments": "This is a test comment for file test.txt"}),
        files=mock_file_upload
    )
    assert response.status_code == 409

# We will come back to this later:
# def test_download(client, mock_access_token, mock_repositories):
#     """ Testing the file download endpoint, does it return a file stream """
#     mock_repositories['bucket'].bucket.find_one.return_value =   {
#         "filename": '4d4331dc8a3006e068ced8f0057dde50.jpg',
#         "chunkSize": 261120,
#     }

#     mock_repositories.['bucket'].bucket.GridOut

#     response = client.get(
#         "/download/testfile.png",
#         headers={"Authorization": "Bearer " + mock_access_token}
#     )

#     assert response


def test_attaching_supporting_evidence_link_to_analysis(
    client,
    mock_access_token,
    mock_repositories,
    cpam0002_analysis_json
):
    """Testing if the supporting evidence gets added to the analysis"""
    def valid_query_side_effect(*args, **kwargs):  # pylint: disable=unused-argument
        find, query = args  # pylint: disable=unused-variable
        analysis = cpam0002_analysis_json
        analysis['supporting_evidence_files'].append(
            query['$push']['supporting_evidence_files'])
        analysis['_id'] = 'fake-mongo-object-id'
        return analysis

    mock_repositories["analysis"].collection.find_one_and_update.side_effect = valid_query_side_effect

    response = client.post(
        "/analysis/CPAM0002/attach/link",
        headers={"Authorization": "Bearer " + mock_access_token},
        data=({
            "link_name": "Interesting Article",
            "link": "http://sites.uab.edu/cgds/",
            "comments": "Serious Things in here",
        })
    )

    result = json.loads(response.text)
    assert len(result['supporting_evidence_files']) == 1
    assert response.status_code == 200


def test_attach_pedigree_image(client, mock_access_token, mock_repositories):
    """ Testing if the create analysis function works with file upload """
    mock_repositories['analysis'].collection.update_one = Mock()
    mock_repositories['bucket'].bucket.put.return_value = "633afb87fb250a6ea1569555"
    mock_repositories["analysis"].collection.find_one.return_value = {
        "_id": ObjectId(str('63430e4f076646300d18bd8d')),
        "sections": [
            {"header": 'Pedigree', "content": []},
        ]
    }

    # This is used here because the 'read_fixture' returns a json dict rather than raw binary
    # We actually want to send a binary file through the endpoint to simulate a file being sent
    # then json.loads is used on the other end in the repository.
    # This'll get updated and broken out in the test_utils in the future
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    path_to_file = os.path.join(
        current_directory, '../fixtures/' + 'pedigree-fake.jpg')

    with open(path_to_file, "rb") as phenotips_file:
        pedigree_image = phenotips_file.read()
        pedigree_bytes = bytearray(pedigree_image)
        response = client.post(
            "/analysis/CPAM0112/attach/pedigree",
            headers={"Authorization": "Bearer " + mock_access_token},
            files={"upload_file": (
                "pedigree-fake.jpg", pedigree_bytes)}
        )

        phenotips_file.close()

    mock_repositories['analysis'].collection.update_one.assert_called_with(
        {'_id': ObjectId('63430e4f076646300d18bd8d')},
        {'$set': {'sections':
                  [{'header': 'Pedigree', 'content': [
                      {
                          'field': 'image', 'value': ["633afb87fb250a6ea1569555"]
                      }]
                    }]
                  }}
    )

    assert response.status_code == 200


def test_get_genomic_units_success(client, mock_access_token, mock_repositories, genomic_unit_success_response):
    """ Testing the get genomic units endpoint """
    mock_repositories["analysis"].collection.find_one.return_value = read_test_fixture(
        "analysis-CPAM0002.json")

    response = client.get("/analysis/CPAM0002/genomic_units",
                          headers={"Authorization": "Bearer " + mock_access_token})

    assert response.status_code == 200
    assert response.json() == genomic_unit_success_response


def test_get_genomic_units_analysis_does_not_exist(client, mock_access_token, mock_repositories):
    """ Testing the get genomic units endpoint """
    mock_repositories["analysis"].collection.find_one.return_value = None

    response = client.get("/analysis/CPAM0002/genomic_units",
                          headers={"Authorization": "Bearer " + mock_access_token})

    assert response.status_code == 404


def test_get_genomic_units_does_not_exist(client, mock_access_token, mock_repositories):
    """ Testing the get genomic units endpoint """
    mock_repositories["analysis"].collection.find_one.return_value = read_test_fixture(
        "analysis-CPAM0002.json").pop("genomic_units")

    response = client.get("/analysis/CPAM0002/genomic_units",
                          headers={"Authorization": "Bearer " + mock_access_token})

    assert response.status_code == 404


@pytest.fixture(name="analysis_updates_json")
def fixture_analysis_updates_json():
    """The JSON that is being sent from a client to the endpoint with updates in it"""
    return read_test_fixture("analysis-update.json")


@pytest.fixture(name="exported_phenotips_to_import_json")
def fixture_phenotips_import():
    """Returns a phenotips json fixture"""
    return read_test_fixture("phenotips-import.json")


@pytest.fixture(name="update_analysis_section_dict")
def fixture_update_analysis_section_json():
    """The JSON that is being sent from a client to the endpoint with updates in it"""
    return {"value": ["the quick brown fox jumps over the lazy dog."]}


@pytest.fixture(name="update_analysis_section_response_json")
def fixture_update_analysis_section_response_json():
    """The JSON that is being sent from a client to the endpoint with updates in it"""
    return read_test_fixture("update_analysis_section.json")


@pytest.fixture(name="genomic_unit_success_response")
def fixture_genomic_unit_success_response():
    """The JSON that is being sent from a client to the endpoint with updates in it"""
    return {
        "genes": {
            "VMA21": [
                "NM_001017980.3:c.164G>T(p.Gly55Val)"
            ],
            "DMD": []
        },
        "variants": [
            "NM_001017980.3:c.164G>T(p.Gly55Val)"
        ]
    }
