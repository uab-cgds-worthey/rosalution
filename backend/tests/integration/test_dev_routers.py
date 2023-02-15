"""Authentication Routes Intergration test"""
from unittest.mock import patch


@patch("src.security.security.verify_password")
def test_dev_login(mock_verify_password, client, mock_repositories):
    """ Tests the dedicated developer login function """
    expected_user = {
        "username": "UABProvider", "scope": ['fakescope'], "client_id": "fake-uab-client-id",
        "hashed_password": "fake-hashed-password"
    }

    mock_repositories['user'].collection.find_one.return_value = expected_user

    mock_verify_password.verify_password.return_value = True

    response = client.post(
        "/dev/loginDev?grant_type=password&username=developer&password=secret",
        headers={"accept": "application/json", 'Content-Type': 'application/x-www-form-urlencoded'},
        json="grant_type=password&username=UABProvider&password=secret"
    )

    assert response.status_code == 200
    assert response.json()['token_type'] == 'bearer'
