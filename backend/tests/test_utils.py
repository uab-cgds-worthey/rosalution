"""General test utilities for the application"""
import json
import os

from unittest.mock import AsyncMock, MagicMock

DATABSE_FIXTURE_PATH = "../../etc/fixtures/initial-seed/"
UNIT_TEST_FIXTURE_PATH = "./fixtures/"
ASSETS_FIXTURE_PATH = f"{UNIT_TEST_FIXTURE_PATH}assets/"


def rosalution_filepath():
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    return os.path.join(current_directory, '../../')


def fixture_path():
    """Returns the fixture data binary"""
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    return os.path.join(current_directory, UNIT_TEST_FIXTURE_PATH)


def integration_database_fixture_filepath():
    """Returns the fixture data binary"""
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    return os.path.join(current_directory, UNIT_TEST_FIXTURE_PATH + "integration-mongodb-database/")


def assets_fixture_filepath(filename):
    """Returns the fixture data binary"""
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    return os.path.join(current_directory, ASSETS_FIXTURE_PATH + filename)


def fixture_filepath(filename):
    """Returns the fixture data binary"""
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    return os.path.join(current_directory, ASSETS_FIXTURE_PATH + filename)


def read_assset_fixture(fixture_name):
    return read_fixtures(ASSETS_FIXTURE_PATH, fixture_name)


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


def magic_mock_mongo_collection():
    """
    Returns the annotation collection for the configuration to verify
    annotation tasks are created according to the configuration
    """
    mock_collection = MagicMock()
    mock_collection.aggregate = MagicMock()
    mock_collection.find = MagicMock()
    mock_collection.find_one = MagicMock()
    mock_collection.update_one = MagicMock()
    mock_collection.insert_one = MagicMock()
    mock_collection.find_one_and_update = MagicMock()
    mock_collection.count_documents = MagicMock()
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


# Disabling PyLint due to this being a simple Mock adapter as a simple test harness for emulating mising a dependency
class SkipDependencies:  # pylint: disable=too-few-public-methods
    """ A skip annotation dependencies helper class that allows tester to dictate which datasets to skip once to
    emulate a depedency not existing the first time when preparing an Annotation Task for annotation."""

    def __init__(self, dependencies_to_skip=None):
        """ Dictating the list of  of dataset names to emulate that dataset annotation not existing."""
        self.skip_tracker = {}
        self.to_skip = dependencies_to_skip if dependencies_to_skip else ["HGNC_ID"]
        self.mock_manifest_entry = {
            "data_set": "mock-dataset", "data_source": "mock-datasource", "version": "fake-version"
        }

    def set_analysis_manifest_entry(self, dependency_manifest_entry: dict):
        self.mock_manifest_entry = dependency_manifest_entry

    async def skip_find_genomic_unit_annotation_value_mock(self, *args):
        """ Mock method that tracks if the provided dependencies are one of the ones indicated to skip"""
        annotation_unit = args[0]
        name = annotation_unit.get_dataset_name()
        genomic_unit = annotation_unit.get_genomic_unit()
        should_skip = (name in self.to_skip and name not in self.skip_tracker)
        return self.skip_tracker.setdefault(name, None) if should_skip else f"{genomic_unit}-{name}-value"

    async def skip_get_manifest_entry_analysis(self, *args):
        """ Mock method that tracks if the provided dependencies are one of the ones indicated to skip"""
        analysis_name, genomic_unit, dataset_name = args
        if dataset_name not in self.to_skip:
            return None

        should_skip = dataset_name not in self.skip_tracker
        return self.skip_tracker.setdefault(dataset_name, None) if should_skip else self.mock_manifest_entry
