import pytest


# Define a parameterized test that covers different scenarios for reconnect API.
# Each scenario includes a set of headers (headers) and the expected HTTP status code (expected_status_code).
@pytest.mark.parametrize("headers, expected_status_code", 
    [
        ({"content-type": "application/json", "token": "valid_token"}, 200), # Reconnect successfully with valid token
        ({"content-type": "application/json", "token": "invalid_token"}, 400), # Reconnect with an invalid token
        ({"content-type": "application/json"}, 401), # Reconnect without a token (Unauthorized)
    ]
)

# The (test_auth_reconnect) function is a single test that covers all scenarios by iterating through the headers and checking the response status code.
def test_auth_reconnect(client, headers, expected_status_code):
    """Test auth reconnect API with different scenarios"""
    response = client.get(
        "/api/auth/reconnect",
        headers=headers,
    )

    assert response.status_code == expected_status_code