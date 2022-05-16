"""Test Fixtures for integration tests"""
from unittest.mock import Mock
import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.database import Database
from src.dependencies import database, annotation_queue


@pytest.fixture(name='client', scope='class')
def test_application_client():
    """A class scoped FastApi Test Client"""
    return TestClient(app)


@pytest.fixture(name='mock_annotation_queue', scope='class')
def mock_queue():
    """A mocked Python queue used to verify if annotation tasks are created"""
    annotation_queue.annotation_queue = Mock()
    return annotation_queue.annotation_queue


@pytest.fixture(name='database_collections', scope='class')
def mock_database_collections():
    """A mocked database client which overrides the database depedency injected """
    mock_database_client = Mock()
    mock_database_client.db = {
        'analysis': Mock(),
        'annotation': Mock()
    }
    mock_database = Database(mock_database_client)
    app.dependency_overrides[database] = mock_database
    yield mock_database_client.db
    app.dependency_overrides.clear()
