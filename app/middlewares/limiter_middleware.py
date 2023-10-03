from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


"""
Flask-Limiter allows setting rate limits for specific routes or globally for your Flask application. 
The code initializes Flask-Limiter and sets a rate limit of 50 requests per minute for all routes.
`get_remote_address` key function limits requests based on the remote IP address
"""
limiter = Limiter(
    key_func = get_remote_address,
    storage_uri = "redis://localhost:6379",
    storage_options={"socket_connect_timeout": 30},
    strategy="fixed-window", # or "moving-window"
    default_limits = ["50 per minute"]
)