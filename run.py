import os
from dotenv import load_dotenv
from os.path import join, dirname, abspath, pardir

from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

from app.db import db
from app.middlewares.limiter_middleware import limiter
from app.routes.auth_routes import blueprint_auth
from app.routes.oauth_routes import blueprint_oauth
from app.routes.board_routes import blueprint_board
from app.routes.list_routes import blueprint_list
from app.routes.task_routes import blueprint_task
from app.routes.priority_routes import blueprint_priority
from app.config import DevelopmentConfig


# Load environment variables from .env file
load_dotenv(join(dirname(__file__), pardir, '.env'))

def create_app():
    # Flask app initialization
    app = Flask(__name__, template_folder="templates")

    # Api initialization
    api_prefix = "/api"
    blueprint_swagger = get_swaggerui_blueprint(base_url=api_prefix, api_url="/static/swagger.json")
    
    # Configuration settings
    app.config.from_object(DevelopmentConfig)  # Use `get_app_config` to select the appropriate configuration

    # Register extensions
    db.init_app(app)
    limiter.init_app(app)
    CORS(app)

    # Register each of the blueprints to the Flask application
    app.register_blueprint(blueprint_swagger, url_prefix=api_prefix)
    app.register_blueprint(blueprint_auth, url_prefix=api_prefix)
    app.register_blueprint(blueprint_oauth, url_prefix=api_prefix)
    app.register_blueprint(blueprint_board, url_prefix=api_prefix)
    app.register_blueprint(blueprint_list, url_prefix=api_prefix)
    app.register_blueprint(blueprint_task, url_prefix=api_prefix)
    app.register_blueprint(blueprint_priority, url_prefix=api_prefix)

    return app

if __name__=="__main__":
    app = create_app()
    app.app_context().push() # Push the app context
    db.create_all() # Create the database tables
    app.run() # Run the application in debug mode
