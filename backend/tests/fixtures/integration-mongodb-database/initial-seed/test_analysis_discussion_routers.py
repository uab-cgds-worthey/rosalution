"""Testing endpoints for adding/updating/removing discussion messages to an analysis."""

import json
import pytest


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories", "mock_security_get_project_authorization")
async def test_add_new_discussion_to_analysis(client, mock_access_token_header):
    """ Testing that a discussion was added and returned properly """
    cpam_analysis = "CPAM0002"
    new_post_content = ["Integration Test Text"]

    response = await client.post(
        "/analysis/" + cpam_analysis + "/discussions",
        headers=mock_access_token_header,
        data={
            "discussion_content": new_post_content,
            "attachments":
                json.dumps({
                    "attachments": [{
                        "attachment_id": "existing-id-0123", "name": "best website", "data": "http://a03.org"
                    }]
                }),
            "file_attachments": [],
        }
    )

    assert response.status_code == 200

    assert len(response.json()) == 4

    actual_most_recent_post = response.json().pop()
    assert actual_most_recent_post['author_fullname'] == 'Developer'
    assert actual_most_recent_post['content'] == new_post_content


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories", "mock_security_get_project_authorization")
async def test_update_discussion_post_in_analysis(client, mock_access_token):
    """ Tests successfully updating an existing post in the discussions with the user being the author """
    cpam_analysis = "CPAM0002"
    discussion_post_id = "9027ec8d-6298-4afb-add5-6ef710eb5e98"
    discussion_content = ["I am an integration test post. Look at me!"]

    response = await client.put(
        "/analysis/" + cpam_analysis + "/discussions/" + discussion_post_id,
        headers={"Authorization": "Bearer " + mock_access_token, "Content-Type": "application/json"},
        content=json.dumps(discussion_content)
    )

    assert response.status_code == 200

    actual_post = None
    for d in response.json():

        if d['post_id'] == discussion_post_id:
            actual_post = d

    assert len(response.json()) == 3
    assert actual_post['content'] == discussion_content


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories", "mock_security_get_project_authorization")
async def test_update_post_in_analysis_author_mismatch(client, mock_access_token):
    """ Tests updating a post that the author did not post and results in an unauthorized failure """
    cpam_analysis = "CPAM0047"
    discussion_post_id = "b2023fa7-b598-416a-9f42-862c826255ef"
    discussion_content = ["I am an integration test post. Look at me!"]

    response = await client.put(
        "/analysis/" + cpam_analysis + "/discussions/" + discussion_post_id,
        headers={"Authorization": "Bearer " + mock_access_token, "Content-Type": "application/json"},
        content=json.dumps(discussion_content)
    )

    expected_failure_detail = {'detail': 'User cannot update post they did not author.'}

    assert response.status_code == 401
    assert response.json() == expected_failure_detail


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories", "mock_security_get_project_authorization")
async def test_delete_discussion_post_in_analysis(client, mock_access_token):
    """ Tests successfully deleting an existing post in the discussions with the user being the author """
    cpam_analysis = "CPAM0002"
    discussion_post_id = "e6023fa7-b598-416a-9f42-862c826255ef"

    response = await client.delete(
        "/analysis/" + cpam_analysis + "/discussions/" + discussion_post_id,
        headers={"Authorization": "Bearer " + mock_access_token}
    )

    assert len(response.json()) == 2


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories", "mock_security_get_project_authorization")
async def test_delete_discussion_post_with_thread(client, mock_access_token):
    """ Tests successfully deleting an existing post in the discussions with the user being the author """
    cpam_analysis = "CPAM0002"
    discussion_post_id = "a677bb36-acf8-4ff9-a406-b113a7952f7e"

    response = await client.delete(
        "/analysis/" + cpam_analysis + "/discussions/" + discussion_post_id,
        headers={"Authorization": "Bearer " + mock_access_token}
    )

    actual_posts = response.json()
    assert len(actual_posts) == 3
    discussion_post = next((post for post in actual_posts if post["post_id"] == discussion_post_id), None)

    assert discussion_post is not None
    assert len(discussion_post["content"]) == 0
    assert discussion_post["author_fullname"] == ""


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories", "mock_security_get_project_authorization")
async def test_delete_discussion_with_attachments(client, mock_access_token):
    """ Tests successfully deleting an existing post in the discussions with the user being the author """
    cpam_analysis = "CPAM0002"
    discussion_post_id = "9027ec8d-6298-4afb-add5-6ef710eb5e98"

    response = await client.delete(
        "/analysis/" + cpam_analysis + "/discussions/" + discussion_post_id,
        headers={"Authorization": "Bearer " + mock_access_token}
    )

    assert len(response.json()) == 2

    # TODO: Return to implement way to query gridfs if files exists.  Files do not exist in fixtures currently.
    # expected_objectid_string = ["68a761c9bd16bc0a0c98062e", "68a761c9bd16bc0a0c98062e"]


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories", "mock_security_get_project_authorization")
async def test_handle_delete_post_not_existing_in_analysis(client, mock_access_token):
    """ Tests failure of deleting a discussion post but does not exist in the analysis  """
    cpam_analysis = "CPAM0002"
    discussion_post_id = "fake-post-id"

    response = await client.delete(
        "/analysis/" + cpam_analysis + "/discussions/" + discussion_post_id,
        headers={"Authorization": "Bearer " + mock_access_token}
    )

    expected_failure_detail = {'detail': f"Post '{discussion_post_id}' does not exist."}

    assert response.status_code == 404
    assert response.json() == expected_failure_detail


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories", "mock_security_get_project_authorization")
async def test_add_new_discussion_reply_to_analysis(client, mock_access_token):
    """ Testing that a discussion reply was added and returned properly """

    # TODO.- Create a different mock access token for a different mock user than 'Developer'

    cpam_analysis = "CPAM0002"
    new_reply_user = "Developer"
    discussion_post_id = "9027ec8d-6298-4afb-add5-6ef710eb5e98"
    new_reply_content = ["Integration Test Text."]

    response = await client.post(
        "/analysis/" + cpam_analysis + "/discussions/" + discussion_post_id + "/thread/",
        headers={"Authorization": "Bearer " + mock_access_token},
        data={
            "discussion_reply_content": new_reply_content,
            "reply_attachments":
                json.dumps({
                    "attachments": [{
                        "attachment_id": "existing-id-0123", "name": "best website", "data": "http://a03.org"
                    }]
                }),
            "reply_attachment_files": [],
        }
    )

    assert response.status_code == 200

    discussion_post = next(
        (item for item in response.json() if item['post_id'] == '9027ec8d-6298-4afb-add5-6ef710eb5e98'), None
    )
    thread = discussion_post['thread']

    assert len(thread) == 1

    actual_most_recent_reply = thread.pop()

    assert actual_most_recent_reply['author_fullname'] == new_reply_user
    assert actual_most_recent_reply['content'] == new_reply_content


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories", "mock_security_get_project_authorization")
async def test_update_discussion_reply_in_analysis(client, mock_access_token):
    """ Testing that a discussion reply was edited, updated and returned properly """

    # TOOD - Update the mock access token to be a different user then 'Developer'

    cpam_analysis = "CPAM0002"
    discussion_post_id = "a677bb36-acf8-4ff9-a406-b113a7952f7e"
    discussion_reply_id = "79057545a-554e-44f7-9553-8d622710e303"
    edit_reply_content = ["EDIT: Integration Test Text."]

    response = await client.post(
        "/analysis/" + cpam_analysis + "/discussions/" + discussion_post_id + "/thread/" + discussion_reply_id,
        headers={"Authorization": "Bearer " + mock_access_token, "Content-Type": "application/json"},
        content=json.dumps(edit_reply_content)
    )
    assert response.status_code == 200

    discussion_post = next((item for item in response.json() if item['post_id'] == discussion_post_id), None)
    actual_most_recent_reply = discussion_post['thread'].pop()

    assert actual_most_recent_reply['content'] == edit_reply_content


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories", "mock_security_get_project_authorization")
async def test_delete_discussion_reply_from_analysis(client, mock_access_token):
    """ Tests successfully deleting an existing reply in the discussions with the user being the author """
    cpam_analysis = "CPAM0002"
    discussion_post_id = "a677bb36-acf8-4ff9-a406-b113a7952f7e"
    discussion_reply_id = "6905754b-554e-44f7-9553-8d622710e303"

    response = await client.delete(
        "/analysis/" + cpam_analysis + "/discussions/" + discussion_post_id + "/thread/" + discussion_reply_id,
        headers={"Authorization": "Bearer " + mock_access_token},
    )

    discussion_post = next((item for item in response.json() if item['post_id'] == discussion_post_id), None)

    assert len(discussion_post['thread']) == 1

    discussion_reply = next((reply for reply in discussion_post["thread"] if reply['reply_id'] == discussion_reply_id),
                            None)

    assert discussion_reply is None
