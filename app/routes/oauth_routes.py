import jwt
import requests

from flask import Blueprint, current_app, jsonify, request

from ..db import db
from ..models import User


blueprint_oauth = Blueprint("oauth", __name__)

@blueprint_oauth.route("/oauth/github", methods=["POST"])
def github_signup():
    request_data = request.get_json()

    user_code = request_data.get("code")
    user_state = request_data.get("state")

    # Check for the existence of GitHub OAuth credentials
    github_client_id = current_app.config.get("GITHUB_CLIENT_ID")
    github_client_secret = current_app.config.get("GITHUB_CLIENT_SECRET")

    if not (github_client_id and github_client_secret):
        return jsonify(msg="GitHub OAuth credentials are missing"), 500
    
    github_login_oauth_url = "https://github.com/login/oauth/access_token"

    github_params = {
        "client_id": github_client_id,
        "client_secret": github_client_secret,
        "code": user_code,
        "state": user_state,
    }

    # Request access token from GitHub
    github_access_token = requests.post(github_login_oauth_url, params=github_params)

    if github_access_token.status_code != 200:
        return jsonify(msg="Failed to get access token from GitHub"), 401
    
    access_token = github_access_token.json().get("access_token")

    if not access_token:
        return jsonify(msg="Failed to retrieve access token from GitHub response"), 401
    
    headers = {
        "Authorization": f"token {access_token}"
    }

    github_user_url = "https://api.github.com/user"

    # Request user info from GitHub
    github_user_info = requests.get(github_user_url, headers=headers)

    if github_user_info.status_code != 200:
        return jsonify(msg="Failed to retrieve user info from Github"), 401
    
    user_data = github_user_info.json()
    primary_email = None

    github_user_emails_url = "https://api.github.com/user/emails"

    # Request user emails from GitHub
    github_user_emails_info = requests.get(github_user_emails_url, headers=headers)

    if github_user_emails_info.status_code == 200:
        github_user_emails_response = github_user_emails_info.json()
        primary_email_data = next((email for email in github_user_emails_response if email.get("primary")), None)

        if primary_email_data:
            primary_email = primary_email_data.get("email")

    # Check if the user already exists
    user =  User.query.filter_by(email=primary_email).first()

    if not user:
        # Create a new user if does not exist
        new_user = User(username=user_data["login"], email=primary_email, strategy="GITHUB")

        db.session.add(new_user)
        db.session.commit()

    # Generate and encode a JSON Web Token (JWT) for the user
    token_payload = {
        "id": user.id,
        "username": user.username,
        "strategy": user.strategy,
        "created_at": user.created_at   # Encoding the JWT token, keep the key names consistent with the naming conventions. For example, use `created_at` instead of `createdAt` for consistency. The payload will match the expected payload when decoding the token.
    }

    secret_key = current_app.config.get("SECRET_KEY")

    token_signature = jwt.encode(
        token_payload,
        secret_key,
        algorithm="HS256"
    ).decode("utf-8")

    response_data = {
        **token_payload,
        "token": token_signature
    }

    return jsonify(response_data), 200

    