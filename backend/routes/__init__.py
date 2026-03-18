"""Register all Blueprints onto the Flask application."""

from flask import Flask

from routes.articles import articles_bp
from routes.comments import comments_bp
from routes.system import system_bp


def register_blueprints(app: Flask) -> None:
    """Attach every route Blueprint with the correct URL prefix."""
    app.register_blueprint(articles_bp, url_prefix="/api/articles")

    # Comments are nested under articles: /api/articles/<id>/comments
    app.register_blueprint(
        comments_bp,
        url_prefix="/api/articles/<int:article_id>/comments",
    )
    
    # System settings route
    app.register_blueprint(system_bp, url_prefix="/api/system")
