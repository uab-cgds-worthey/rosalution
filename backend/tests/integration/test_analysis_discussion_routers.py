"""Testing endpoints for adding/updating/removing discussion messages to an analysis."""

import json
import pytest
from bson import ObjectId


def test_add_new_discussion_to_analysis(client, mock_access_token, mock_repositories, cpam0002_analysis_json):
    """ Testing that a discussion was added and returned properly """
    cpam_analysis = "CPAM0002"
    new_post_user = "John Doe"
    new_post_content = ["Integration Test Text"]

    def valid_query_side_effect(*args, **kwargs):  # pylint: disable=unused-argument
        find, query = args  # pylint: disable=unused-variable
        analysis = cpam0002_analysis_json
        analysis['discussions'].append(query['$push']['discussions'])
        analysis['_id'] = 'fake-mongo-object-id'
        return analysis

    mock_repositories["user"].collection.find_one.return_value = {"full_name": new_post_user}
    mock_repositories['analysis'].collection.find_one.return_value = cpam0002_analysis_json
    mock_repositories["analysis"].collection.find_one_and_update.side_effect = valid_query_side_effect

    response = client.post(
        "/analysis/" + cpam_analysis + "/discussions",
        headers={"Authorization": "Bearer " + mock_access_token},
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

    assert actual_most_recent_post['author_fullname'] == new_post_user
    assert actual_most_recent_post['content'] == new_post_content


def test_update_discussion_post_in_analysis(client, mock_access_token, mock_repositories, cpam0002_analysis_json):
    """ Tests successfully updating an existing post in the discussions with the user being the author """
    cpam_analysis = "CPAM0002"
    discussion_post_id = "fake-post-id"
    discussion_content = ["I am an integration test post. Look at me!"]

    # Inject a new discussion post by John Doe
    def valid_query_side_effect_one(*args, **kwargs):  # pylint: disable=unused-argument
        analysis = cpam0002_analysis_json

        new_discussion_post = {
            "post_id": "fake-post-id", "author_id": "johndoe-client-id", "author_fullname": 'johndoe',
            "content": ["Hello, I am a discussion post."],
            "attachments": [{"attachment_id": "existing-id-0123", "name": "best website", "data": "http://a03.org"}]
        }

        analysis['discussions'].append(new_discussion_post)
        analysis['_id'] = 'fake-mongo-object-id'
        return analysis

    def valid_query_side_effect_two(*args, **kwargs):  # pylint: disable=unused-argument
        find, query = args  # pylint: disable=unused-variable
        query_filter = kwargs

        analysis = cpam0002_analysis_json
        fake_post_content = query['$set']['discussions.$[item].content']
        fake_post_id = query_filter['array_filters'][0]['item.post_id']

        for d in analysis['discussions']:
            if d['post_id'] == fake_post_id:
                d['content'] = fake_post_content

        analysis['_id'] = 'fake-mongo-object-id'

        return analysis

    mock_repositories['analysis'].collection.find_one.side_effect = valid_query_side_effect_one
    mock_repositories["analysis"].collection.find_one_and_update.side_effect = valid_query_side_effect_two

    response = client.put(
        "/analysis/" + cpam_analysis + "/discussions/" + discussion_post_id,
        headers={"Authorization": "Bearer " + mock_access_token},
        content=json.dumps(discussion_content)
    )

    actual_post = None

    for d in response.json():

        if d['post_id'] == discussion_post_id:
            actual_post = d

    assert len(response.json()) == 4
    assert actual_post['content'] == discussion_content


def test_update_post_in_analysis_author_mismatch(client, mock_access_token, mock_repositories, cpam0002_analysis_json):
    """ Tests updating a post that the author did not post and results in an unauthorized failure """
    cpam_analysis = "CPAM0002"
    discussion_post_id = "9027ec8d-6298-4afb-add5-6ef710eb5e98"
    discussion_content = ["I am an integration test post. Look at me!"]

    mock_repositories['analysis'].collection.find_one.return_value = cpam0002_analysis_json

    response = client.put(
        "/analysis/" + cpam_analysis + "/discussions/" + discussion_post_id,
        headers={"Authorization": "Bearer " + mock_access_token},
        content=json.dumps(discussion_content)
    )

    expected_failure_detail = {'detail': 'User cannot update post they did not author.'}

    assert response.status_code == 401
    assert response.json() == expected_failure_detail


def test_delete_discussion_post_in_analysis(client, mock_access_token, mock_repositories, cpam0002_analysis_json):
    """ Tests successfully deleting an existing post in the discussions with the user being the author """
    cpam_analysis = "CPAM0002"
    discussion_post_id = "e6023fa7-b598-416a-9f42-862c826255ef"

    def remove_discussion_from_fixture(*args, **kwargs):  # pylint: disable=unused-argument
        find, query = args  # pylint: disable=unused-variable

        analysis = cpam0002_analysis_json
        fake_post_id = query['$pull']['discussions']['post_id']

        analysis['discussions'] = [x for x in analysis['discussions'] if fake_post_id not in x['post_id']]
        analysis['_id'] = 'fake-mongo-object-id'

        return analysis

    mock_repositories['analysis'].collection.find_one.return_value = cpam0002_analysis_json
    mock_repositories["analysis"].collection.find_one_and_update.side_effect = remove_discussion_from_fixture

    response = client.delete(
        "/analysis/" + cpam_analysis + "/discussions/" + discussion_post_id,
        headers={"Authorization": "Bearer " + mock_access_token}
    )

    assert len(response.json()) == 2


def test_delete_discussion_post_with_thread(client, mock_access_token, mock_repositories, cpam0002_analysis_json):
    """ Tests successfully deleting an existing post in the discussions with the user being the author """
    cpam_analysis = "CPAM0002"
    discussion_post_id = "a677bb36-acf8-4ff9-a406-b113a7952f7e"
    cpam0002_analysis_json["_id"] = "fjkldsjfil;ajkfdlja;f"

    mock_repositories['analysis'].collection.find_one.return_value = cpam0002_analysis_json
    mock_repositories["analysis"].collection.find_one_and_update.return_value = cpam0002_analysis_json

    response = client.delete(
        "/analysis/" + cpam_analysis + "/discussions/" + discussion_post_id,
        headers={"Authorization": "Bearer " + mock_access_token}
    )

    assert len(response.json()) == 3
    assert mock_repositories["analysis"].collection.find_one_and_update.call_count == 1
    actual_filter, actual_update = mock_repositories["analysis"].collection.find_one_and_update.call_args[0]
    assert actual_filter['name'] == "CPAM0002"
    assert len(actual_update['$set']["discussions.$[item].content"]) == 0
    assert actual_update['$set']["discussions.$[item].author_fullname"] == ""
    assert actual_update['$set']["discussions.$[item].deleted"] is True


def test_delete_discussion_with_attachments(client, mock_access_token, mock_repositories, cpam0002_analysis_json):
    """ Tests successfully deleting an existing post in the discussions with the user being the author """
    cpam_analysis = "CPAM0002"
    discussion_post_id = "9027ec8d-6298-4afb-add5-6ef710eb5e98"

    def remove_discussion_from_fixture(*args, **kwargs):  # pylint: disable=unused-argument
        find, query = args  # pylint: disable=unused-variable

        analysis = cpam0002_analysis_json
        fake_post_id = query['$pull']['discussions']['post_id']

        analysis['discussions'] = [x for x in analysis['discussions'] if fake_post_id not in x['post_id']]
        analysis['_id'] = 'fake-mongo-object-id'

        return analysis

    mock_repositories['analysis'].collection.find_one.return_value = cpam0002_analysis_json
    mock_repositories['bucket'].bucket.exists.return_value = True
    mock_repositories["analysis"].collection.find_one_and_update.side_effect = remove_discussion_from_fixture

    response = client.delete(
        "/analysis/" + cpam_analysis + "/discussions/" + discussion_post_id,
        headers={"Authorization": "Bearer " + mock_access_token}
    )

    assert len(response.json()) == 2
    assert mock_repositories["bucket"].bucket.delete.call_count == 1

    actual_removed_file_id = mock_repositories["bucket"].bucket.delete.call_args[0][0]
    assert actual_removed_file_id == ObjectId("68a761c9bd16bc0a0c98062e")


def test_handle_delete_post_not_existing_in_analysis(
    client, mock_access_token, mock_repositories, cpam0002_analysis_json
):
    """ Tests failure of deleting a discussion post but does not exist in the analysis  """
    cpam_analysis = "CPAM0002"
    discussion_post_id = "fake-post-id"

    mock_repositories['analysis'].collection.find_one.return_value = cpam0002_analysis_json

    response = client.delete(
        "/analysis/" + cpam_analysis + "/discussions/" + discussion_post_id,
        headers={"Authorization": "Bearer " + mock_access_token}
    )

    expected_failure_detail = {'detail': f"Post '{discussion_post_id}' does not exist."}

    assert response.status_code == 404
    assert response.json() == expected_failure_detail


def test_add_new_discussion_reply_to_analysis(client, mock_access_token, mock_repositories, cpam0002_analysis_json):
    """ Testing that a discussion reply was added and returned properly """
    cpam_analysis = "CPAM0002"
    new_reply_user = "John Doe"
    discussion_post_id = "9027ec8d-6298-4afb-add5-6ef710eb5e98"
    new_reply_content = ["Integration Test Text."]

    def valid_query_side_effect(*args, **kwargs):
        find, query = args  # pylint: disable=unused-variable
        query_filter = kwargs

        analysis = cpam0002_analysis_json
        fake_post_id = query_filter['array_filters'][0]['item.post_id']
        fake_thread = query['$push']['discussions.$[item].thread']

        modified_discussion = next((item for item in analysis['discussions'] if item['post_id'] == fake_post_id), None)

        modified_discussion['thread'].append(fake_thread)
        analysis['_id'] = 'fake-mongo-object-id'

        return analysis

    mock_repositories["user"].collection.find_one.return_value = {"full_name": new_reply_user}
    mock_repositories['analysis'].collection.find_one.return_value = cpam0002_analysis_json
    mock_repositories["analysis"].collection.find_one_and_update.side_effect = valid_query_side_effect

    response = client.post(
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


def test_update_discussion_reply_in_analysis(client, mock_access_token, mock_repositories, cpam0002_analysis_json):
    """ Testing that a discussion reply was edited, updated and returned properly """
    cpam_analysis = "CPAM0002"
    edit_reply_user = "John Doe"
    discussion_post_id = "9027ec8d-6298-4afb-add5-6ef710eb5e98"
    discussion_reply_id = "fake-reply-id"
    edit_reply_content = ["EDIT: Integration Test Text."]

    # Inject a new discussion reply by John Doe
    def valid_query_side_effect_one(*args, **kwargs):  # pylint: disable=unused-argument
        analysis = cpam0002_analysis_json
        discussion_post_id = "9027ec8d-6298-4afb-add5-6ef710eb5e98"

        new_discussion_reply = {
            "reply_id": "fake-reply-id",
            "author_id": "johndoe-client-id",
            "author_fullname": 'johndoe',
            "content": ["Hello, I am a discussion reply."],
        }

        discussion_post = next((item for item in analysis['discussions'] if item['post_id'] == discussion_post_id),
                               None)
        discussion_post['thread'].append(new_discussion_reply)

        analysis['_id'] = 'fake-mongo-object-id'
        return analysis

    def valid_query_side_effect_two(*args, **kwargs):
        find, query = args  # pylint: disable=unused-variable
        query_filter = kwargs

        analysis = cpam0002_analysis_json

        modified_discussion = next(
            (item for item in analysis['discussions'] if item['post_id'] == "9027ec8d-6298-4afb-add5-6ef710eb5e98"),
            None
        )

        fake_reply_content = query['$set']['discussions.$[post].thread.$[reply].content']
        fake_reply_id = query_filter['array_filters'][1]['reply.reply_id']

        reply_to_update = next((item for item in modified_discussion['thread'] if item['reply_id'] == fake_reply_id),
                               None)
        reply_to_update['content'] = fake_reply_content

        analysis['_id'] = 'fake-mongo-object-id'

        return analysis

    mock_repositories["user"].collection.find_one.return_value = {"full_name": edit_reply_user}
    mock_repositories['analysis'].collection.find_one.return_value = cpam0002_analysis_json
    mock_repositories['analysis'].collection.find_one.side_effect = valid_query_side_effect_one
    mock_repositories["analysis"].collection.find_one_and_update.side_effect = valid_query_side_effect_two

    response = client.post(
        "/analysis/" + cpam_analysis + "/discussions/" + discussion_post_id + "/thread/" + discussion_reply_id,
        headers={"Authorization": "Bearer " + mock_access_token},
        content=json.dumps(edit_reply_content)
    )

    discussion_post = next(
        (item for item in response.json() if item['post_id'] == "9027ec8d-6298-4afb-add5-6ef710eb5e98"), None
    )

    assert response.status_code == 200

    actual_most_recent_reply = discussion_post['thread'].pop()

    assert actual_most_recent_reply['content'] == edit_reply_content


def test_delete_discussion_reply_from_analysis(client, mock_access_token, mock_repositories, cpam0002_analysis_json):
    """ Tests successfully deleting an existing reply in the discussions with the user being the author """
    cpam_analysis = "CPAM0002"
    edit_reply_user = "Developer Person"
    discussion_post_id = "9027ec8d-6298-4afb-add5-6ef710eb5e98"
    discussion_reply_id = "fake-reply-id"

    # Inject a new discussion reply by John Doe
    def valid_query_side_effect_one(*args, **kwargs):  # pylint: disable=unused-argument
        analysis = cpam0002_analysis_json
        discussion_post_id = "9027ec8d-6298-4afb-add5-6ef710eb5e98"

        new_discussion_reply = {
            "reply_id": "fake-reply-id",
            "author_id": "johndoe-client-id",
            "author_fullname": 'johndoe',
            "content": "Hello, I am a discussion reply.",
        }

        discussion_post = next((item for item in analysis['discussions'] if item['post_id'] == discussion_post_id),
                               None)
        discussion_post['thread'].append(new_discussion_reply)

        analysis['_id'] = 'fake-mongo-object-id'
        return analysis

    def valid_query_side_effect_two(*args, **kwargs):  # pylint: disable=unused-argument
        find, query = args  # pylint: disable=unused-variable

        analysis = cpam0002_analysis_json

        modified_discussion = next(
            (item for item in analysis['discussions'] if item['post_id'] == "9027ec8d-6298-4afb-add5-6ef710eb5e98"),
            None
        )

        fake_reply_id = query['$pull']['discussions.$[post].thread']['reply_id']
        # fake_reply_id = query_filter['array_filters'][1]['reply.reply_id']

        modified_discussion['thread'] = [x for x in modified_discussion['thread'] if fake_reply_id not in x['reply_id']]
        analysis['_id'] = 'fake-mongo-object-id'

        return analysis

    mock_repositories["user"].collection.find_one.return_value = {"full_name": edit_reply_user}
    mock_repositories['analysis'].collection.find_one.return_value = cpam0002_analysis_json
    mock_repositories['analysis'].collection.find_one.side_effect = valid_query_side_effect_one
    mock_repositories["analysis"].collection.find_one_and_update.side_effect = valid_query_side_effect_two

    response = client.delete(
        "/analysis/" + cpam_analysis + "/discussions/" + discussion_post_id + "/thread/" + discussion_reply_id,
        headers={"Authorization": "Bearer " + mock_access_token},
    )

    discussion_post = next(
        (item for item in response.json() if item['post_id'] == "9027ec8d-6298-4afb-add5-6ef710eb5e98"), None
    )

    assert len(discussion_post['thread']) == 0


@pytest.fixture(name="get_discussion_json")
def get_analysis_discussion_json():
    """Fixture function to retrieve the json for a single discussion by an analysis"""

    def _get_analysis_discussion_json(analysis_json, post_id: str):
        """Provides the json for an individual discussion from an analysis json fixture"""
        print(analysis_json)
        return next((discussion for discussion in analysis_json['discussions'] if discussion['post_id'] == post_id),
                    None)

    return _get_analysis_discussion_json
