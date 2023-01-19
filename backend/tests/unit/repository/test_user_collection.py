""" Tests to verify users are properly accessed and handled """
import pytest

from src.repository.user_collection import UserCollection

from ...test_utils import mock_mongo_collection


def test_find_all_users(user_collection):
    """Get all the users from the user collection"""
    all_users = user_collection.all()
    assert len(all_users) == 1


def test_find_user_by_username_successful(user_collection):
    """ Gets the user from the user collection using the username """
    username = "johndoe"

    user_collection.find_by_username(username)
    user_collection.collection.find_one.assert_called_with({"username": username})


def test_find_user_by_username_unsuccessful(user_collection):
    """ Handles failing to find a user by username """
    user_collection.collection.find_one.return_value = None
    user = user_collection.find_by_username("johnnybravo")
    assert user is None


def test_find_user_by_client_by_id_successful(user_collection):
    """ Gets the user from the user collection using the client id """
    client_id = "fake-client-id"

    user_collection.find_by_client_id(client_id)
    user_collection.collection.find_one_assert_called_with({"client_id": client_id})


def test_find_user_by_client_by_id_unsuccessful(user_collection):
    """ Handles failing to find a user with a client id """
    user_collection.collection.find_one.return_value = None
    user = user_collection.find_by_client_id("fake-client-id")
    assert user is None


def test_update_client_secret_successful(user_collection):
    """ Updates the existing client secret """
    client_id = "fake-client-id"
    client_secret = "fake-client-secret"

    user_collection.update_client_secret(client_id, client_secret)

    user_collection.collection.find_one_and_update.assert_called_with({'client_id': client_id},
                                                                      {'$set': {'client_secret': client_secret}})


def test_update_client_secret_unsuccessful(user_collection):
    """ Updates the existing client secret """
    client_id = "fake-client-id-not-in-system"
    client_secret = "fake-client-secret-not-in-system"

    user_collection.collection.find_one_and_update.return_value = None

    user = user_collection.update_client_secret(client_id, client_secret)

    user_collection.collection.find_one_and_update.assert_called_with({'client_id': client_id},
                                                                      {'$set': {'client_secret': client_secret}})

    assert user is None


@pytest.fixture(name="user_collection")
def fixture_user_collection(users_json, user_john_doe):
    """ Fixture for the user collection """

    mock_collection = mock_mongo_collection()
    mock_collection.find.return_value = users_json
    mock_collection.find_one.return_value = user_john_doe

    return UserCollection(mock_collection)


@pytest.fixture(name="user_john_doe")
def fixture_user_john_doe(users_json):
    """ Fixture for the user John Doe from the users collection JSON """
    return next((user for user in users_json if user['full_name'] == "John Doe"), None)
