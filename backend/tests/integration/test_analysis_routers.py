"""Analysis Routes Integration test"""

import os
import pytest
from ..test_utils import read_database_fixture, read_test_fixture


def test_get_analyses(client, mock_access_token, database_collections):
    """Testing that the correct number of analyses were returned and in the right order"""
    database_collections['analysis'].collection.find.return_value = read_database_fixture(
        "analyses.json")

    response = client.get(
        "/analysis/", headers={"Authorization": "Bearer " + mock_access_token})

    assert response.status_code == 200
    assert len(response.json()) == 5
    assert response.json()[2]["name"] == "CPAM0047"


def test_get_analyses_unauthorized(client, database_collections):
    """Tries to get the analyses from the endpoint, but is unauthorized. Does not provide valid token"""
    database_collections['analysis'].collection.find.return_value = read_database_fixture(
        "analyses.json")
    response = client.get("/analysis/")

    # This is temporarily changed as security is removed for the analysis endpoints to make development easier
    # assert response.status_code == 401
    assert response.status_code == 200


def test_get_analysis_summary(client, mock_access_token, database_collections):
    """Testing if the analysis summary endpoint returns all of the analyses available"""
    database_collections['analysis'].collection.find.return_value = read_test_fixture(
        "analyses-summary-db-query-result.json")
    response = client.get(
        "/analysis/summary", headers={"Authorization": "Bearer " + mock_access_token})
    assert len(response.json()) == 5


def test_create_analysis(client, mock_access_token, database_collections, exported_phenotips_to_import_json):
    """Testing if the create analysis endpoint creates a new analysis"""
    database_collections["analysis"].collection.insert_one.return_value = True
    database_collections["analysis"].collection.find_one.return_value = None
    database_collections["genomic_unit"].collection.find_one.return_value = None
    response = client.post(
        "/analysis/import",
        headers={"Authorization": "Bearer " + mock_access_token,
                 "Content-Type": "application/json"},
        json=exported_phenotips_to_import_json,
    )
    assert response.status_code == 200

def test_create_analysis_with_file(client, mock_access_token, database_collections):
    """ Testing if the create analysis function works with file upload """
    database_collections["analysis"].collection.insert_one.return_value = True
    database_collections["analysis"].collection.find_one.return_value = None
    database_collections["genomic_unit"].collection.find_one.return_value = None

    # This is used here because the 'read_fixture' returns a json dict rather than raw binary
    # We actually want to send a binary file through the endpoint to simulate a file being sent
    # then json.loads is used on the other end in the repository.
    # This'll get updated and broken out in the test_utils in the future
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    path_to_file = os.path.join(
    current_directory, '../fixtures/' + 'phenotips-import.json')

    with open(path_to_file, "rb") as phenotips_file:
        response  = client.post(
            "/analysis/import_file",
            headers={"Authorization": "Bearer " + mock_access_token},
            files={"phenotips_file": ("phenotips-import.json", phenotips_file.read())}
        )

        phenotips_file.close()

    assert response.status_code == 200

def test_update_analysis(client, mock_access_token, database_collections, analysis_updates_json):
    """Testing if the update analysis endpoint updates an existing analysis"""
    database_collections["analysis"].collection.find_one_and_update.return_value = analysis_updates_json
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


def test_upload_file_to_analysis(client, mock_access_token, mock_file_upload, database_collections):
    """Testing if the upload file endpoint uploads a file to an analysis"""
    # This test currently writes a file to the backend folder, This will eventually be changed to write
    # the mongo database instead with GridFS. We are currently git-ignoring this file to avoid it being commited.
    database_collections["analysis"].collection.find_one_and_update.return_value = {
        'fakevalue': 'fakeyfake'}
    response = client.post(
        "/analysis/upload/CPAM0002",
        headers={"Authorization": "Bearer " + mock_access_token},
        data=({"comments": "This is a test comment for file test.txt"}),
        files=mock_file_upload
    )

    assert response.status_code == 200


@pytest.fixture(name="analysis_updates_json")
def fixture_analysis_updates_json():
    """The JSON that is being sent from a client to the endpoint with updates in it"""
    return read_test_fixture("analysis-update.json")


@ pytest.fixture(name="exported_phenotips_to_import_json")
def fixture_phenotips_import():
    """Returns a phenotips json fixture"""
    return read_test_fixture("phenotips-import.json")
