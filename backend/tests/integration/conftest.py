"""Test Fixtures for integration tests"""
import json
import os
from unittest.mock import Mock
from httpx import ASGITransport, AsyncClient
import pytest
from fastapi.security import OAuth2PasswordBearer
from fastapi.testclient import TestClient
from cas import CASClient
from testcontainers.compose import DockerCompose
from pymongo import AsyncMongoClient
from pymongo.errors import ConnectionFailure
import gridfs
import pytest_asyncio

from src.routers.auth_router import get_cas_client
from src.main import app
from src.database import Database
from src.config import get_settings, Settings
from src.dependencies import get_db, annotation_queue
from src.security.security import create_access_token, get_current_user, get_project_authorization,\
    get_create_project_authorization

from ..test_utils import integration_database_fixture_filepath, read_test_fixture, rosalution_filepath, fixture_path
from fastapi.testclient import TestClient

# import pytest


@pytest.fixture(scope='session')
def anyio_backend():
    return 'asyncio'


@pytest.fixture(name="client", scope='session')
async def test_application_client(anyio_backend):
    """A class scoped FastApi Test Client"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        yield async_client


@pytest.fixture(name="cas_client")
def mock_get_cas_client(mock_settings):
    """Mock settings for enabling teh CAS client mocking for authentication in testing"""
    mock_cas_client = get_cas_client(mock_settings)

    def mock_get() -> CASClient:
        return mock_cas_client

    app.dependency_overrides[get_cas_client] = mock_get
    yield mock_cas_client
    app.dependency_overrides.clear()


@pytest.fixture(name="mock_annotation_queue", scope="class")
def mock_queue():
    """A mocked Python queue used to verify if annotation tasks are created"""
    annotation_queue.annotation_queue = Mock()
    return annotation_queue.annotation_queue


@pytest.fixture(name="async_db_client", scope="session")
async def async_db_client(anyio_backend):
    services = ['rosalution-integration-db']
    with DockerCompose(
        integration_database_fixture_filepath(), compose_file_name="docker-compose.mongodb.yml", services=services
    ) as compose:
        mongodb_connection_uri = f"mongodb://localhost:28017/rosalution_db?replicaSet=rs0&directConnection=true"
        async with AsyncMongoClient(mongodb_connection_uri) as mongodb_async_client:
            bucket = gridfs.asynchronous.AsyncGridFS(mongodb_async_client.rosalution_db)
            live_database = Database(mongodb_async_client, bucket)
            yield live_database


@pytest.fixture(name="mock_repositories")
async def mock_database_collections(async_db_client):
    """A mocked database client which overrides the database depedency injected"""

    def mock_get_db() -> dict:
        return async_db_client()

    app.dependency_overrides[get_db] = mock_get_db
    async with async_db_client.database_client.start_session() as session:
        async with session.bind():
            try:
                await session.start_transaction()
                yield async_db_client.collections
            finally:
                await session.abort_transaction()
        app.dependency_overrides.clear()


@pytest.fixture(name="mock_settings_cas_disabled")
def mock_cas_disabled_application_settings(settings_json):
    """The mocked settings which overrides the applications need for environment variables or .env file"""
    settings_json["cas_login_enable"] = False
    fake_settings = Settings(**settings_json)

    def mock_get_settings():
        return fake_settings

    app.dependency_overrides[get_settings] = mock_get_settings
    yield fake_settings
    app.dependency_overrides.clear()


@pytest.fixture(name="mock_settings", autouse=True)
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


@pytest.fixture(name="mock_security_get_project_authorization")
def mock_get_project_authorization():
    """Mocks user successfully authroizing access to project"""

    def mock_project_authorized():
        return True

    app.dependency_overrides[get_project_authorization] = mock_project_authorized
    yield
    app.dependency_overrides.clear()


@pytest.fixture(name="mock_security_get_create_project_authorization")
def mock_get_create_project_authorization(mock_security_get_current_user):
    """Mocks user successfully authorizing the user has write permissions to the project"""

    def mock_create_analysis_authorized():
        return (mock_security_get_current_user, "CPAM")

    app.dependency_overrides[get_create_project_authorization] = mock_create_analysis_authorized
    yield
    app.dependency_overrides.clear()


@pytest.fixture(name="mock_user")
def test_auth_user():
    """A mocked user that can be used to generate an OAuth2 access token"""
    return {"sub": "3bghhsmnyqi6uxovazy07ryn9q1tqbnt", "scopes": ["read", "write"]}


@pytest.fixture(name="mock_access_token_header")
def mock_access_token_header(mock_access_token: str) -> dict[str, str]:
    """Mocks a valid access token for the tests to properly execute"""
    return {"Authorization": f"Bearer {mock_access_token}"}


@pytest.fixture(name="mock_access_token")
def mock_access_token_str(mock_user, mock_settings):
    """Mocks a valid access token for the tests to properly execute"""
    user_data_to_encode = mock_user
    return create_access_token(
        user_data_to_encode,
        mock_settings.oauth2_access_token_expire_minutes,
        mock_settings.rosalution_key,
        mock_settings.oauth2_algorithm,
    )


@pytest.fixture(name="settings_json")
def fixture_settings_json():
    """Returns the settings for a fake rosalution. Mostly used for security functionality/testing"""
    return read_test_fixture("application_settings.shared.json")
