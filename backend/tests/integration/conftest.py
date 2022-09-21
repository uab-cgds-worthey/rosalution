"""Test Fixtures for integration tests"""
import os
from unittest.mock import Mock
import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.database import Database
from src.dependencies import database, annotation_queue
from src.security.jwt import create_access_token

from ..test_utils import mock_mongo_collection


@pytest.fixture(name="client", scope="class")
def test_application_client():
    """A class scoped FastApi Test Client"""
    return TestClient(app)


@pytest.fixture(name="mock_annotation_queue", scope="class")
def mock_queue():
    """A mocked Python queue used to verify if annotation tasks are created"""
    annotation_queue.annotation_queue = Mock()
    return annotation_queue.annotation_queue


@pytest.fixture(name="database_collections", scope="class")
def mock_database_collections():
    """A mocked database client which overrides the database depedency injected"""
    mock_database_client = Mock()
    mock_database_client.rosalution_db = {
        "analyses": mock_mongo_collection(),
        "annotations_config": mock_mongo_collection(),
        "genomic_units": mock_mongo_collection(),
        "users": mock_mongo_collection()
    }
    mock_database = Database(mock_database_client)
    app.dependency_overrides[database] = mock_database
    yield mock_database.collections
    app.dependency_overrides.clear()


@pytest.fixture(name="mock_user")
def test_auth_user():
    """A mocked user that can be used to generate an OAuth2 access token"""
    return {"sub": "johndoe", "scopes": ["read", "write"]}


@pytest.fixture(name="mock_access_token")
def mock_access_token(mock_user):
    """Mocks a valid access token for the tests to properly execute"""
    return create_access_token(data=mock_user, expires_delta=None)


@pytest.fixture(name="mock_file_upload")
def mock_file_upload():
    """A mocked file upload"""
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    path_to_file = os.path.join(
        current_directory, '../fixtures/' + 'example_file_to_upload.txt')
    return {"upload_file": ('example_file_to_upload.txt', open(path_to_file, 'rb'))}
