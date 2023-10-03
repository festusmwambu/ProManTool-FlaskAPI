import json
import pytest


# Define a parameterized test that covers different scenarios for creating a new board.
# Each scenario includes a set of parameters (params), headers (headers), and the expected HTTP status code (expected_status_code).
@pytest.mark.parametrize("params, headers, expected_status_code",
    [
        ({"boardName": "My new board"}, {"content-type": "application/json", "token": "valid_token"}, 200), # Request successful with valid parameters and token
        ({}, {"content-type": "application/json", "token": "valid_token"}, 400), # Request with missing parameters
        ({}, {"content-type": "application/json"}, 401), # Request without a token (Unauthorized)
        ({}, {"content-type": "application/json", "token": "invalid_token"}, 400), # Request with an invalid token
    ]
)

# The (test_create_board) function is a single test that covers all scenarios by iterating through the parameters, headers, and checking the response status code.
def test_create_board(client, params, headers, expected_status_code):
    """Test creating a new board with different scenarios"""
    response = client.post(
        "/api/boards/new",
        data=json.dumps(params),
        headers=headers
    )

    assert response.status_code == expected_status_code