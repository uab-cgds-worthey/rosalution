""" Tests to verify users are properly accessed and handled """
import pytest

from src.repository.user_collection import UserCollection

from ...test_utils import mock_mongo_collection


def test_find_all_users(user_collection):
    """Get all the users from the user collection"""
    all_users = user_collection.all()
    assert len(all_users) == 1


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
