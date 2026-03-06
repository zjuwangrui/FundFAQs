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

    now = _now()
    with get_db() as conn:
        article = conn.execute("SELECT id FROM articles WHERE id = ?", (article_id,)).fetchone()
        if not article:
            return jsonify({"error": "文章不存在"}), 404

        cur = conn.execute(
            "INSERT INTO comments (article_id, commenter, content, created_at) VALUES (?, ?, ?, ?)",
            (article_id, commenter, content, now),
        )
        row = conn.execute("SELECT * FROM comments WHERE id = ?", (cur.lastrowid,)).fetchone()

    return jsonify(dict(row)), 201


if __name__ == "__main__":
    app.run(debug=True, port=5000)
