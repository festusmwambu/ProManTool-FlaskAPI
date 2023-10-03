import os
import jwt
import pytest

from dotenv import load_dotenv
from os.path import abspath, dirname, join

from ..run import create_app


# Load environment variables from .env file
load_dotenv(join(dirname(__file__), abspath(".."), ".env"))


# Define the `app` fixture, which creates the Flask app instance
@pytest.fixture
def app():
    app = create_app()
    return app


# Define `client` fixture, which uses the `app` fixture to create a test client
@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def valid_token():
    token_payload = {
        "id": 11,
        "username": "test_user",
        "password": "test_password",
    }

    secret_key = os.environ.get("SECRET_KEY")

    token_signature = jwt.encode(
        token_payload,
        secret_key,
        algorithm="HS256"
    ).decode("utf-8")

    return token_signature


@pytest.fixture
def invalid_token():
    token_payload = {
        "id": 11,
        "username": "test_user",
        "password": "test_password",
    }

    token_signature = jwt.encode(
        token_payload,
        "INVALID KEY",
        algorithm="HS256"
    ).decode("utf-8")

    return token_signature