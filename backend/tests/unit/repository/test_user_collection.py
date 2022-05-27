""" Tests to verify users are properly accessed and handled """
import pytest

from src.repository.user_collection import UserCollection

def test_find_all_users(user_collection):
    """ Get all the users from the user collection """
    all_users = user_collection.all()
    assert len(all_users.keys()) == 1

def test_find_specific_user_successful(user_collection):
    """ Get all the users from the user collection """
    user = user_collection.find_by_name('johndoe')
    assert user['full_name'] == "John Doe"
    assert user['email'] == "johndoe@example.com"

def test_find_specific_user_unsuccessful(user_collection):
    """ Get all the users from the user collection """
    user = user_collection.find_by_name('johnnybravo')
    assert user is None

def test_authenticate_user_successful(user_collection):
    """ Get all the users from the user collection """
    user = user_collection.authenticate_user('johndoe', 'secret')

    assert user['full_name'] == "John Doe"
    assert user['email'] == "johndoe@example.com"

def test_authenticate_user_unsuccessful_no_user(user_collection):
    """ Get all the users from the user collection """
    user = user_collection.authenticate_user('johndoe', 'secret1')

    assert user is False

def test_authenticate_user_unsuccessful_password(user_collection):
    """ Get all the users from the user collection """
    user = user_collection.authenticate_user('johndoe', 'secret1')

    assert user is False

@pytest.fixture(name="user_collection")
def fixture_user_collection():
    """ Fixture for the user collection """
    return UserCollection()
