import pytest


# Define a parameterized test that covers different scenarios for getting priorities.
# Each scenario includes headers (headers) and the expected HTTP status code (expected_status_code).
@pytest.mark.parametrize("headers, expected_status_code", 
    [
        ({"content-type": "application/json", "token": "valid_token"}, 200), # Request successful with a valid token
        ({"content-type": "application/json"}, 401), # Request without a token (Unauthorized)
        ({"content-type": "application/json", "token": "valid_token"}, 400), # Request with an invalid token 
    ]
)

# The (test_get_priorities) function is a single test that covers all scenarios by iterating through the headers and checking the response status code.
def test_get_priorities(client, headers, expected_status_code):
    """Test retrieving priorities with different scenarios"""
    response = client.get(
        "/api/priorities",
        headers=headers,
    )

    assert response.status_code == expected_status_code