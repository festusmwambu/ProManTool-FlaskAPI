import os


# `Config` is the base configuration class that contains common configuration settings for all the entire application. 
class Config:
    DEBUG=False
    TESTING=False
    CORS_HEADERS="Content-Type"
    SECRET_KEY=os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///promantooldev.db")

# `ProductionConfig` class inherits from `Config` base class and sets the `SQLALCHEMY_DATABASE_URI` from the `DATABASE_URL` environment variable, which is suitable for production environment.
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI=os.getenv("PRODUCTION_DATABASE_URL")

# `DevelopmentConfig` class inherits from `Config` base class and sets a default `SQLALCHEMY_DATABASE_URI` suitable for development environment 
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///promantooldev.db")
# `TestingConfig` class inherits from `Config` base class and sets a default `SQLALCHEMY_DATABASE_URI` suitable for testing environment 
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI=os.getenv("TESTING_DATABASE_URL")
