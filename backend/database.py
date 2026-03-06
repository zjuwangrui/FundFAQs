"""Database helpers: connection factory and schema initialisation."""

import sqlite3

from config import active_config


def get_db() -> sqlite3.Connection:
    """Open a new SQLite connection with Row factory enabled."""
    conn = sqlite3.connect(active_config.DATABASE)
    conn.row_factory = sqlite3.Row
    # Enforce foreign key constraints
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    """Create tables if they do not already exist."""
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS articles (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                title      TEXT    NOT NULL,
                content    TEXT    NOT NULL,
                created_at TEXT    NOT NULL,
                updated_at TEXT    NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS comments (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                article_id INTEGER NOT NULL,
                commenter  TEXT    NOT NULL DEFAULT '匿名',
                content    TEXT    NOT NULL,
                created_at TEXT    NOT NULL,
                FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE
            )
            """
        )
