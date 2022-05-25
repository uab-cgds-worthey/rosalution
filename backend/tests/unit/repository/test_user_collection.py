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
    assert user == None

def test_authenticate_user_successful(user_collection):
    """ Get all the users from the user collection """
    user = user_collection.authenticate_user('johndoe', 'secret')
    
    assert user['full_name'] == "John Doe"
    assert user['email'] == "johndoe@example.com"

def test_authenticate_user_unsuccessful_no_user(user_collection):
    """ Get all the users from the user collection """
    user = user_collection.authenticate_user('johndoe', 'secret1')
    
    assert user == False

def test_authenticate_user_unsuccessful_password(user_collection):
    """ Get all the users from the user collection """
    user = user_collection.authenticate_user('johndoe', 'secret1')
    
    assert user == False

@pytest.fixture(name="user_collection")
def fixture_user_collection():
    """ Fixture for the user collection """
    return UserCollection()

# @pytest.fixture(name='users')
# def users_fixture():
#     """ Fixtures of various users in the system """
#     return {
#         "johndoe": {
#             "username": "johndoe",
#             "full_name": "John Doe",
#             "email": "johndoe@example.com",
#             "scope": "modify",
#             "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
#             "disabled": False
#         }
#     }
