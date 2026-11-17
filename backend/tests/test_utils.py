"""General test utilities for the application"""
import json
import os

from unittest.mock import AsyncMock, MagicMock

DATABSE_FIXTURE_PATH = "../../etc/fixtures/initial-seed/"
FIXTURE_PATH = "./fixtures/"
ASSETS_FIXTURE_PATH = f"{FIXTURE_PATH}assets/"


def integration_database_fixture_path():
    """Returns the path to the integration-mongodb-database directory"""
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    return os.path.join(current_directory, FIXTURE_PATH + "integration-mongodb-database/")


def assets_fixture_filepath(filename):
    """Returns the fixture data binary"""
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    return os.path.join(current_directory, ASSETS_FIXTURE_PATH + filename)


def read_assset_fixture(fixture_name):
    """reads the text file from the assests fixture path"""
    return read_fixtures(ASSETS_FIXTURE_PATH, fixture_name)


def read_test_fixture(fixture_filename):
    """reads the JSON from the filepath relative to the tests"""
    return read_fixtures(FIXTURE_PATH, fixture_filename)


def read_fixtures(base_path, fixture_filename):
    """With a base path relative to the current directory, loads a fixture for fixture_filename"""
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    path_to_file = os.path.join(current_directory, base_path + fixture_filename)
    with open(path_to_file, mode="r", encoding="utf-8") as file_to_open:
        data = json.load(file_to_open)
        file_to_open.close()

    return data


def mock_mongo_collection():
    """
    Returns the annotation collection for the configuration to verify
    annotation tasks are created according to the configuration
    """
    fake_mongodb_cursor = AsyncMock()
    fake_mongodb_cursor.to_list.return_value = []
    mock_collection = AsyncMock()
    mock_collection.aggregate = AsyncMock()
    mock_collection.find = AsyncMock(return_value=fake_mongodb_cursor)
    mock_collection.find_one = AsyncMock()
    mock_collection.update_one = AsyncMock()
    mock_collection.insert_one = AsyncMock()
    mock_collection.find_one_and_update = AsyncMock()
    mock_collection.count_documents = AsyncMock()
    return mock_collection


def mock_gridfs_bucket():
    """Returns a mocked GridFS bucket"""
    mock_bucket = AsyncMock()
    mock_bucket.open_download_stream = AsyncMock()
    mock_bucket.open_upload_stream = AsyncMock()
    mock_bucket.put = AsyncMock()
    mock_bucket.get = AsyncMock()
    mock_bucket.list = AsyncMock()
    mock_bucket.exists = AsyncMock()
    mock_bucket.delete = AsyncMock()
    return mock_bucket


def magic_mock_gridfs_bucket():
    """Returns a mocked GridFS bucket"""
    mock_bucket = MagicMock()
    mock_bucket.open_download_stream = MagicMock()
    mock_bucket.open_upload_stream = MagicMock()
    mock_bucket.put = MagicMock()
    mock_bucket.get = MagicMock()
    mock_bucket.list = MagicMock()
    mock_bucket.exists = MagicMock()
    mock_bucket.delete = MagicMock()
    return mock_bucket
