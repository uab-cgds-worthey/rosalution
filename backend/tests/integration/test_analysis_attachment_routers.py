"""Testing endpoints for adding/updating/removing document and link attachments to an analysis."""

import json
import pytest


def test_attaching_link_to_analysis(client, mock_access_token, mock_repositories, cpam0002_analysis_json):
    """Test attaching a URL to the analysis"""

    def valid_query_side_effect(*args, **kwargs):  # pylint: disable=unused-argument
        find, query = args  # pylint: disable=unused-variable
        analysis = cpam0002_analysis_json
        analysis['attachments'].append(query['$push']['attachments'])
        analysis['_id'] = 'fake-mongo-object-id'
        return analysis

    new_attachment = {
        "link_name": "Interesting Article",
        "link": "http://sites.uab.edu/cgds/",
        "comments": "Serious Things in here",
    }

    mock_repositories["analysis"].collection.find_one_and_update.side_effect = valid_query_side_effect

    response = client.post(
        "/analysis/CPAM0002/attachment",
        headers={"Authorization": "Bearer " + mock_access_token},
        data={'new_attachment': json.dumps(new_attachment)}
    )

    assert response.status_code == 200
    actual_attachments = json.loads(response.text)
    assert len(actual_attachments) == 2


def test_remove_file_attachment(client, mock_access_token, mock_repositories, cpam0002_analysis_json):
    """ Testing the remove a file attachment endpoint """
    mock_repositories["bucket"].bucket.exists.return_value = True
    mock_repositories["analysis"].collection.find_one.return_value = cpam0002_analysis_json
    mock_repositories["analysis"].collection.find_one_and_update.return_value = cpam0002_analysis_json

    response = client.delete(
        "/analysis/CPAM0002/attachment/633afb87fb250a6ea1569555",
        headers={"Authorization": "Bearer " + mock_access_token}
    )

    assert response.status_code == 200

    mock_repositories['bucket'].bucket.exists.assert_called()
    mock_repositories['bucket'].bucket.delete.assert_called()

    save_call_args = mock_repositories["analysis"].collection.find_one_and_update.call_args[0]
    (actual_name, actual_update_query) = save_call_args
    assert actual_name['name'] == "CPAM0002"
    assert len(actual_update_query['$set']['attachments']) == 0


def test_remove_link_attachment(
    client, mock_access_token, mock_repositories, cpam0002_analysis_json_with_link_attachment
):
    """ Testing the remove link attachment endpoint """
    mock_repositories["bucket"].bucket.exists.return_value = False
    mock_repositories["analysis"].collection.find_one.return_value = cpam0002_analysis_json_with_link_attachment
    mock_repositories["analysis"
                     ].collection.find_one_and_update.return_value = cpam0002_analysis_json_with_link_attachment

    response = client.delete(
        "/analysis/CPAM0002/attachment/a1ea5c7e-1c13-4d14-a3d7-297f39f11ba8",
        headers={"Authorization": "Bearer " + mock_access_token}
    )

    assert response.status_code == 200
    save_call_args = mock_repositories["analysis"].collection.find_one_and_update.call_args[0]
    (actual_name, actual_update_query) = save_call_args
    assert actual_name['name'] == "CPAM0002"

    assert len(actual_update_query['$set']['attachments']) == 0


@pytest.fixture(name="cpam0002_analysis_json_with_link_attachment")
def fixture_attachment_link_json(cpam0002_analysis_json):
    """The JSON that is being returned to the endpoint with a link in the attachments"""
    cpam0002_analysis_json["attachments"] = [{
        "name": "this is a silly link name", "data": "http://local.rosalution.cgds/rosalution/api/docs",
        "attachment_id": "a1ea5c7e-1c13-4d14-a3d7-297f39f11ba8", "type": "link", "comments": "hello link world"
    }]
    return cpam0002_analysis_json
