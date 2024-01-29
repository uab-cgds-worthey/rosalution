"""Testing endpoints for adding/updating/removing document and link attachments to an analysis."""

import json
import pytest

from ..test_utils import read_test_fixture


def test_attaching_supporting_evidence_link_to_analysis(
    client, mock_access_token, mock_repositories, cpam0002_analysis_json
):
    """Testing if the supporting evidence gets added to the analysis"""

    def valid_query_side_effect(*args, **kwargs):  # pylint: disable=unused-argument
        find, query = args  # pylint: disable=unused-variable
        analysis = cpam0002_analysis_json
        analysis['supporting_evidence_files'].append(query['$push']['supporting_evidence_files'])
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


def test_remove_supporting_evidence_file(client, mock_access_token, mock_repositories):
    """ Testing the remove attachment endpoint """
    mock_repositories["bucket"].bucket.exists.return_value = True
    mock_repositories["analysis"].collection.find_one.return_value = read_test_fixture("analysis-CPAM0002.json")
    expected = read_test_fixture("analysis-CPAM0002.json")
    expected["supporting_evidence_files"] = []
    mock_repositories["analysis"].collection.find_one_and_update.return_value = expected

    response = client.delete(
        "/analysis/CPAM0002/attachment/633afb87fb250a6ea1569555/remove",
        headers={"Authorization": "Bearer " + mock_access_token}
    )

    mock_repositories['bucket'].bucket.exists.assert_called()
    mock_repositories['bucket'].bucket.delete.assert_called()
    assert response.status_code == 200
    assert response.json() == expected


def test_remove_supporting_evidence_link(client, mock_access_token, mock_repositories, supporting_evidence_link_json):
    """ Testing the remove attachment endpoint """
    mock_repositories["bucket"].bucket.exists.return_value = False
    mock_repositories["analysis"].collection.find_one.return_value = supporting_evidence_link_json
    expected = read_test_fixture("analysis-CPAM0002.json")
    expected["supporting_evidence_files"] = []
    mock_repositories["analysis"].collection.find_one_and_update.return_value = expected

    response = client.delete(
        "/analysis/CPAM0002/attachment/a1ea5c7e-1c13-4d14-a3d7-297f39f11ba8/remove",
        headers={"Authorization": "Bearer " + mock_access_token}
    )

    assert response.status_code == 200
    assert response.json() == expected


@pytest.fixture(name="supporting_evidence_link_json")
def fixture_supporting_evidence_link_json():
    """The JSON that is being returned to the endpoint with a link in the supporting evidence"""
    setup_return_value = read_test_fixture("analysis-CPAM0002.json")
    setup_return_value["supporting_evidence_files"] = [{
        "name": "this is a silly link name", "data": "http://local.rosalution.cgds/rosalution/api/docs",
        "attachment_id": "a1ea5c7e-1c13-4d14-a3d7-297f39f11ba8", "type": "link", "comments": "hello link world"
    }]
    return setup_return_value
