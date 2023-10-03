from functools import wraps
from flask import current_app, g, jsonify, request
import jwt


"""
The code below is a common pattern for protecting routes in Flask using JWT(JSON Web Tokens) for authentication.
It wraps a route function and checks for a valid token in the request header.
"""
def protected_route(route): 
    @wraps(route)
    def wrapper(*args, **kwargs):
        # Contents of the Authorization header - (Authorization: Bearer <token>)
        bearer_token = request.headers["Authorization"]

        if bearer_token: 
            try: 
                # Extract the token part from the Authorization header using split("Bearer "). This is a common convention for sending JWTs in the header, where the token is preceded by the word "Bearer."
                token_payload = bearer_token.split("Bearer ")[1] # Extract the token part
                
                # `current_app` from Flask is used to access the application configuration, including the `SECRET_KEY`. This is a more Flask-like way to access the configuration values.
                secret_key = current_app.config["SECRET_KEY"]

                # If the token_part is valid, it decodes it and stores the user information in the Flask g object, allowing access to the protected route.
                token_signature = jwt.decode(
                    token_payload, 
                    secret_key, 
                    algorithms="HS256"
                )
                
                g.user = token_signature

                return route(*args, **kwargs)
            
            except jwt.ExpiredSignatureError:
                return jsonify(msg="Token has expired"), 401
            except jwt.InvalidTokenError:
                return jsonify(msg="Invalid token"), 400
            
        return jsonify(msg="Unauthorized, missing token"), 401
    
    return wrapper