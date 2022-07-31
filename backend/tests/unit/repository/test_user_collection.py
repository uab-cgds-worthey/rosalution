""" Tests to verify users are properly accessed and handled """
import pytest

from src.repository.user_collection import UserCollection

from ...test_utils import mock_mongo_collection, read_database_fixture


def test_find_all_users(user_collection):
    """Get all the users from the user collection"""
    all_users = user_collection.all()
    assert len(all_users) == 14


def test_find_specific_user_successful(user_collection):
    """Get all the users from the user collection"""
    user = user_collection.find_by_username("johndoe")
    assert user["full_name"] == "John Doe"
    assert user["email"] == "johndoe@example.com"


def test_find_specific_user_unsuccessful(user_collection):
    """Get all the users from the user collection"""
    user_collection.collection.find_one.return_value = None
    user = user_collection.find_by_username("johnnybravo")
    assert user is None


def test_authenticate_user_successful(user_collection):
    """Get all the users from the user collection"""
    user = user_collection.authenticate_user("johndoe", "secret")

    assert user["full_name"] == "John Doe"
    assert user["email"] == "johndoe@example.com"


def test_authenticate_user_unsuccessful_no_user(user_collection):
    """Get all the users from the user collection"""
    user_collection.collection.find_one.return_value = None
    authenticate_result = user_collection.authenticate_user(
        "johndoe", "secret1")

    assert authenticate_result is False


def test_authenticate_user_unsuccessful_password(user_collection, user_john_doe):
    """Get all the users from the user collection"""
    user_collection.collection.find_one.return_value = user_john_doe
    authenticate_result = user_collection.authenticate_user(
        "johndoe", "secret1")

    assert authenticate_result is False


@pytest.fixture(name="user_collection")
def fixture_user_collection(users_json, user_john_doe):
    """Fixture for the user collection"""

    mock_collection = mock_mongo_collection()
    mock_collection.find.return_value = users_json
    mock_collection.find_one.return_value = user_john_doe

    return UserCollection(mock_collection)


@pytest.fixture(name="user_john_doe")
def fixture_user_john_doe(users_json):
    """Fixture for the user John Doe from the users collection JSON"""
    return next((user for user in users_json if user['full_name'] == "John Doe"), None)


@pytest.fixture(name="users_json")
def fixture_users_json():
    """Returns the JSON for the users collection used to seed the MongoDB database"""
    return read_database_fixture("users.json")
