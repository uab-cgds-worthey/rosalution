"""Analysis Routes Intergration test"""

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
