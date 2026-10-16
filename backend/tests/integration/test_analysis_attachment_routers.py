"""Testing endpoints for adding/updating/removing document and link attachments to an analysis."""

import json
import pytest

@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories")
@pytest.mark.usefixtures("mock_security_get_project_authorization")
async def test_attaching_link_to_analysis(client, mock_access_token):
    """Test attaching a URL to the analysis"""

    new_attachment = {
        "link_name": "Interesting Article",
        "link": "http://sites.uab.edu/cgds/",
        "comments": "Serious Things in here",
    }

    response = await client.post(
        "/analysis/CPAM0002/attachment",
        headers={"Authorization": "Bearer " + mock_access_token},
        data={'new_attachment': json.dumps(new_attachment)}
    )

    assert response.status_code == 200
    actual_attachments = json.loads(response.text)
    assert len(actual_attachments) == 2

@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories")
@pytest.mark.usefixtures("mock_security_get_project_authorization")
async def test_remove_file_attachment(client, mock_access_token):
    """ Testing the remove a file attachment endpoint """

    response = await client.delete(
        "/analysis/CPAM0002/attachment/633afb87fb250a6ea1569555",
        headers={"Authorization": "Bearer " + mock_access_token}
    )

    assert response.status_code == 200

    actual_attachments = json.loads(response.text)
    assert len(actual_attachments) == 0


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories")
@pytest.mark.usefixtures("mock_security_get_project_authorization")
async def test_remove_link_attachment(client, mock_access_token):
    """ Testing the remove link attachment endpoint """

    response = await client.delete(
        "/analysis/CPAM0047/attachment/a1ea5c7e-1c13-4d14-a3d7-297f39f11ba8",
        headers={"Authorization": "Bearer " + mock_access_token}
    )

    assert response.status_code == 200

    actual_attachments = json.loads(response.text)
    assert len(actual_attachments) == 0
