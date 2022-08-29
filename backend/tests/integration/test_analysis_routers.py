"""Analysis Routes Integration test"""

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


# this is a work in progress
def test_update_analysis(client, mock_access_token, database_collections):
    """Testing if the update analysis endpoint updates an existing analysis"""
    database_collections["analysis"].collection.find_one.return_value = read_test_fixture(
        "analysis-CPAM0112.json")  # this is the analysis to update and also the fixture needs to be created
    database_collections["analysis"].collection.update_one.return_value = True
    response = client.put(
        "/analysis/update/CPAM0112",
        headers={"Authorization": "Bearer " + mock_access_token,
                 "Content-Type": "application/json"},
        # this is the new analysis data
        json=read_test_fixture("analyses-update.json"),
    )
    assert response.status_code == 200


@pytest.fixture(name="exported_phenotips_to_import_json")
def fixture_phenotips_import():
    """Returns a phenotips json fixture"""
    return read_test_fixture("phenotips-import.json")
