"""General test utilities for the application"""
import json
import os
import mongomock

from unittest.mock import Mock, MagicMock

DATABSE_FIXTURE_PATH = "../../etc/fixtures/initial-seed/"
UNIT_TEST_FIXTURE_PATH = "./fixtures/"


def read_database_fixture(fixture_filename):
    """reads the JSON from the filepath relative to the database fixtures in etc"""
    return read_fixtures(DATABSE_FIXTURE_PATH, fixture_filename)


def read_test_fixture(fixture_filename):
    """reads the JSON from the filepath relative to the tests"""
    return read_fixtures(UNIT_TEST_FIXTURE_PATH, fixture_filename)


def read_fixtures(base_path, fixture_filename):
    """With a base path relative to the current directory, loads a fixture for fixture_filename"""
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    path_to_file = os.path.join(
        current_directory, base_path + fixture_filename)
    with open(path_to_file, mode="r", encoding="utf-8") as file_to_open:
        data = json.load(file_to_open)
        file_to_open.close()

    return data


def mock_mongo_collection():
    """
    Returns the annotation collection for the configuration to verify
    annotation tasks are created according to the configuration
    """
    mock_collection = Mock()
    mock_collection.find = Mock()
    mock_collection.find_one = Mock()
    mock_collection.update_one = Mock()
    mock_collection.insert_one = Mock()
    mock_collection.find_one_and_update = Mock()
    return mock_collection


def magic_mock_mongo_collection():
    """
    Returns the annotation collection for the configuration to verify
    annotation tasks are created according to the configuration
    """
    mock_collection = MagicMock()
    mock_collection.find = MagicMock()
    mock_collection.find_one = MagicMock()
    mock_collection.update_one = MagicMock()
    mock_collection.insert_one = MagicMock()
    mock_collection.find_one_and_update = MagicMock()
    return mock_collection


def mongomock_collection():
    """
    Returns the annotation collection for the configuration to verify
    annotation tasks are created according to the configuration
    """
    mock_collection = mongomock.MongoClient().db.collection
    return mock_collection
