"""General test utilities for the application"""
import json
import os

from unittest.mock import Mock, MagicMock

DATABSE_FIXTURE_PATH = "../../etc/fixtures/initial-seed/"
UNIT_TEST_FIXTURE_PATH = "./fixtures/"


def fixture_filepath(filename):
    """Returns the fixture data binary"""
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    return os.path.join(current_directory, UNIT_TEST_FIXTURE_PATH + filename)


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


def mock_gridfs_bucket():
    """Returns a mocked GridFS bucket"""
    mock_bucket = Mock()
    mock_bucket.open_download_stream = Mock()
    mock_bucket.open_upload_stream = Mock()
    mock_bucket.put = Mock()
    mock_bucket.get = Mock()
    mock_bucket.list = Mock()
    mock_bucket.exists = Mock()
    mock_bucket.delete = Mock()
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

    def skip_hgncid_get_value_first_time_mock(self, *args):
        """ Mock method that tracks if the provided dependencies are one of the ones indicated to skip"""
        annotation_unit = args[0]
        name = annotation_unit.get_dataset_name()
        genomic_unit = annotation_unit.get_genomic_unit()
        should_skip = (name in self.to_skip and name not in self.skip_tracker)
        return self.skip_tracker.setdefault(name, None) if should_skip else f"{genomic_unit}-{name}-value"
