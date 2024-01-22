"""Test Fixtures for integration tests"""
import os
from unittest.mock import Mock
import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.database import Database
from src.config import get_settings, Settings
from src.dependencies import database, annotation_queue
from src.security.security import create_access_token, get_current_user

from ..test_utils import mock_mongo_collection, mock_gridfs_bucket, read_database_fixture, read_test_fixture


@pytest.fixture(name="client", scope="class")
def test_application_client():
    """A class scoped FastApi Test Client"""
    return TestClient(app)


@pytest.fixture(name="mock_annotation_queue", scope="class")
def mock_queue():
    """A mocked Python queue used to verify if annotation tasks are created"""
    annotation_queue.annotation_queue = Mock()
    return annotation_queue.annotation_queue


@pytest.fixture(name="mock_repositories", scope="class")
def mock_database_collections():
    """A mocked database client which overrides the database depedency injected"""
    mock_database_client = Mock()
    mock_gridfs_client = Mock()

    mock_database_client.rosalution_db = {
        "analyses": mock_mongo_collection(),
        "annotations_config": mock_mongo_collection(),
        "genomic_units": mock_mongo_collection(),
        "users": mock_mongo_collection(),
        "bucket": mock_gridfs_bucket(),
    }

    mock_database = Database(mock_database_client, mock_gridfs_client)
    app.dependency_overrides[database] = mock_database
    yield mock_database.collections
    app.dependency_overrides.clear()


@pytest.fixture(name="mock_settings")
def mock_application_settings(settings_json):
    """The mocked settings which overrides the applications need for environment variables or .env file"""
    fake_settings = Settings(**settings_json)

    def mock_get_settings():
        return fake_settings

    app.dependency_overrides[get_settings] = mock_get_settings
    yield fake_settings
    app.dependency_overrides.clear()


@pytest.fixture(name="mock_security_get_current_user")
def mock_get_current_user(mock_user):
    """The mocked current user to ovveride the get_current_user dependency"""

    def mock_current_user():
        return mock_user["sub"]

    app.dependency_overrides[get_current_user] = mock_current_user
    yield mock_user["sub"]
    app.dependency_overrides.clear()


@pytest.fixture(name="mock_user")
def test_auth_user():
    """A mocked user that can be used to generate an OAuth2 access token"""
    return {"sub": "johndoe-client-id", "scopes": ["read", "write"]}


@pytest.fixture(name="mock_access_token")
def mock_access_token(mock_user, mock_settings):
    """Mocks a valid access token for the tests to properly execute"""
    user_data_to_encode = mock_user
    return create_access_token(
        user_data_to_encode,
        mock_settings.oauth2_access_token_expire_minutes,
        mock_settings.rosalution_key,
        mock_settings.oauth2_algorithm,
    )


@pytest.fixture(name="mock_file_upload")
def mock_file_upload():
    """A mocked file upload"""
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    path_to_file = os.path.join(current_directory, '../fixtures/' + 'example_file_to_upload.txt')
    return {"upload_file": ('example_file_to_upload.txt', open(path_to_file, 'rb'))}


@pytest.fixture(name="cpam0002_analysis_json")
def fixture_cpam0002_analysis_json():
    """The JSON for the CPAM 0002 Analysis"""
    collection = read_database_fixture("analyses.json")
    return next((analysis for analysis in collection if analysis['name'] == "CPAM0002"), None)


@pytest.fixture(name="users_json")
def fixture_users_json():
    """Returns the JSON for the users collection used to seed the MongoDB database"""
    return read_test_fixture("users-test-fixture.json")


@pytest.fixture(name="settings_json")
def fixture_settings_json():
    """Returns the settings for a fake rosalution. Mostly used for security functionality/testing"""
    return read_test_fixture("application_settings.json")
