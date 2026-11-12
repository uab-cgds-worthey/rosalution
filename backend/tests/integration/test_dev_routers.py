"""Authentication Routes Intergration test"""
from unittest.mock import patch
import pytest


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories")
@patch("src.security.security.verify_password")
async def test_dev_login(mock_verify_password, client):
    """ Tests the dedicated developer login function """
    mock_verify_password.verify_password.return_value = True

    response = await client.post(
        "/dev/loginDev?grant_type=password&username=developer&password=secret",
        headers={"accept": "application/json", 'Content-Type': 'application/x-www-form-urlencoded'},
        json="grant_type=password&username=developer&password=secret"
    )

    assert response.status_code == 200
    assert response.json()['token_type'] == 'bearer'
