import bcrypt
import datetime
import jwt

from flask import Blueprint, current_app, g, jsonify, request
from sqlalchemy.exc import IntegrityError

from ..models import User
from ..db import db
from ..middlewares.limiter_middleware import limiter
from ..middlewares.protected_route_middleware import protected_route


blueprint_auth = Blueprint("auth", __name__)

"""
Authentication login route endpoint
"""
@blueprint_auth.route("/auth/login", methods=["POST"])
@limiter.limit("25/5minute")
def login(): 
    request_data = request.get_json()

    username = request_data.get("username")
    password = request_data.get("password")

    if not username or not password:
        return jsonify(msg="Missing required parameters"), 400
    
    user = User.query.filter_by(username=username, strategy="AUTH").first()

    if not user:
        return jsonify(msg="Username does not exist"), 404
    
    verify_password = bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8"))
    
    if verify_password:
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=7)

        token_payload = {
            "id": user.id,
            "username": user.username,
            "exp": expiration_time
        }

        # `current_app.config.get('SECRET_KEY')`is used to retrieve the secret key from the Flask application's configuration, which is a more Flask-like approach.
        secret_key = current_app.config.get("SECRET_KEY")

        token_signature = jwt.encode(
            token_payload,
            secret_key,
            algorithm="HS256"
        ).decode("utf-8")

        response_data = {
            **token_payload,
            "msg": "Login successful",
            "token": token_signature
        }

        return jsonify(response_data), 200
    
    else: 
        return jsonify(msg="Invalid password"), 401
    


"""
Authentication signup route endpoint
"""
@blueprint_auth.route("/auth/signup", methods=["POST"])
@limiter.limit("5/30minute")
def signup():
    request_data = request.get_json()

    username = request_data.get("username")
    password = request_data.get("password")

    if not username or not password:
        return jsonify(msg="Missing required parameters"), 400
    
    user_exists = User.query.filter_by(username=username).first()

    if user_exists:
        return jsonify(msg="Username already exists and is taken"), 400
    
    hashed_password = bcrypt.hashpw(
        password.encode("utf8"),
        bcrypt.gensalt(5)
    ).decode("utf8")

    new_user = User(username=username, password=hashed_password, strategy="AUTH")

    try: 
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

        return jsonify(msg="Username already exists and is taken"), 400

    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=7)

    token_payload = {
        "id": new_user.id,
        "username": new_user.username,
        "created_at": new_user.created_at,
        "exp": expiration_time
    }

    # `current_app.config.get('SECRET_KEY')`is used to retrieve the secret key from the Flask application's configuration, which is a more Flask-like approach.
    secret_key = current_app.config.get("SECRET_KEY")

    token_signature = jwt.encode(
        token_payload,
        secret_key,
        algorithm="HS256",
    ).decode("utf-8")

    response_data = {
        **token_payload,
        "token": token_signature
    }

    return jsonify(response_data), 200



"""
Authentication reconnect route endpoint
"""
@blueprint_auth.route("/auth/reconnect", methods=["POST"])
@protected_route
def reconnect():
    # The decoded and stored user information in the Flask g object, allows access to the protected route.
    # Directly access the `g.user` dictionary instead of extracting `username` and `id` separately from it. This simplifies the code and avoids unnecessary dictionary access.
    id = g.user.get("id")
    username = g.user.get("username")

    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=7)

    # Build the `token_payload` dictionary before encoding the JWT to improve readability
    token_payload = {
        "id": id,
        "username": username,
        "exp": expiration_time
    }

    # `current_app.config.get('SECRET_KEY')`is used to retrieve the secret key from the Flask application's configuration, which is a more Flask-like approach.
    secret_key = current_app.config.get("SECRET_KEY")

    # Build the encoded `token_signature`
    token_signature = jwt.encode(
        token_payload,
        secret_key,
        algorithm="HS256",
    ).decode("utf-8")

    response_data = {
        "id": id,
        "username": username,
        "token": token_signature
    }

    return jsonify(response_data), 200 