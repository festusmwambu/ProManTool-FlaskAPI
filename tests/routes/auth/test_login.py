import json
import pytest


# Define a parameterized test that covers different scenarios for auth login.
# Each scenario includes a set of parameters (params) and the expected HTTP status code (expected_status_code).
@pytest.mark.parametrize("params, expected_status_code", 
    [
        ({"username": "test_user", "password": "test_password"}, 200), # Successful login
        ({"username": "test_user", "password": "invalidpassword123"}, 401), # Invalid password
        ({"username": "nonexistent_user_in_db", "password": "whatever"}, 404), # User not found
        ({}, 400), # Missing required parameters: Username and Password
        ({"username": "test_user"}, 400), # Missing required parameter: Password
        ({"password": "test_password"}, 400), # Missing required parameter: Username
    ]
)

# The (test_auth_login) function is a single test that covers all scenarios by iterating through the parameters and checking the response status code.
def test_auth_login(client, params, expected_status_code):
    """Test auth login API endpoint with different scenarios"""
    headers = {
        "content-type": "application/json",
    }

    response = client.post(
        "api/auth/login",
        data=json.dumps(params), 
        headers=headers
    )

    assert response.status_code == expected_status_code