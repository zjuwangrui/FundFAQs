"""Application factory and entry point."""

from flask import Flask
from flask_cors import CORS

from config import active_config
from database import init_db
from routes import register_blueprints



def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    CORS(app, origins=active_config.CORS_ORIGINS)

    # Initialise database schema
    init_db()

    # Register all route Blueprints
    register_blueprints(app)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=active_config.DEBUG, port=5000)
