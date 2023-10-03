import pytest


# Define a parametrized test that covers different scenarios for the boards API.
# Each scenario includes a set of headers (headers) and the expected HTTP status code (expected_status_code).
@pytest.mark.parametrize("headers, expected_status_code", 
    [
        ({"content-type": "application/json", "token": "valid_token"}, 200), # Request successful with a valid token
        ({"content-type": "application/json", "token": "invalid_token"}, 400), # Request with an invalid token
        ({"content-type": "application/json"}, 401), # Request withut a token (Unauthorized)
    ]
)

# The (test_get_boards) function is a single test that covers all scenarios by iterating through the parameters and checking the response status code.
def test_get_boards(client, headers, expected_status_code):
    """Test boards API with different scenarios"""
    response = client.get(
        "/api/boards",
        headers=headers,
    )

    assert response.status_code == expected_status_code
    