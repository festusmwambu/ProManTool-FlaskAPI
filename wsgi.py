from run import create_app

# =============================================================================================================================
# This module contains the code that is used for running Flask app in production environment mode.
# =============================================================================================================================

# Import the code from `run.py` module.
app = create_app()

if __name__ == "__main__":
    app.app_context().push()

    from app.db import db # Push the app context
    db.create_all() # Create the database tables

    app.run(debug=False) # Run the application in production environment mode.