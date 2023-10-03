import json
import pytest


# Define a parameterized test that covers different scenarios for auth signup.
# Each scenario includes a set of parameters (params) and the expected HTTP status code (expected_status_code).
@pytest.mark.parametrize("params, expected_status_code", 
    [
        ({}, 400), # Missing required parameters: Username and Password
        ({"username": "test_user"}, 400), # Missing required parameter: Password
        ({"password": "test_password"}, 400), # Missing required parameter: Username
    ]
)

# The (test_auth_signup) function is a single test that covers all scenarios by iterating through the parameters and checking the response status code.
def test_auth_signup(client, params, expected_status_code):
    """Test auth signup API endpoint with different scenarios"""
    headers = {
        "content-type": "application/json",
    }

    response = client.post(
        "api/auth/signup",
        data=json.dumps(params),
        headers=headers
    )

    assert response.status_code == expected_status_code

    