"""Application configuration."""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config:
    """Base configuration shared by all environments."""

    DEBUG: bool = False

    # SQLite database file path
    DATABASE: str = os.path.join(BASE_DIR, "fund_faqs.db")

    # Pagination defaults & limits
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 100
    DEFAULT_COMMENT_PAGE_SIZE: int = 20

    # Field length constraints
    MAX_TITLE_LENGTH: int = 200
    MAX_COMMENT_LENGTH: int = 1000
    MAX_COMMENTER_LENGTH: int = 50

    # CORS – in production restrict to actual frontend origin
    CORS_ORIGINS: str = "*"

    # Admin secret for protected article operations (update/delete).
    # In production, override via environment variable FUNDFAQ_ADMIN_SECRET.
    ADMIN_SECRET: str = os.getenv("FUNDFAQ_ADMIN_SECRET", "CHANGE_ME_FUNDFAQ_ADMIN_SECRET")


class DevelopmentConfig(Config):
    DEBUG: bool = True


class ProductionConfig(Config):
    DEBUG: bool = False


# Active configuration resolved from environment variable
_env = os.getenv("FLASK_ENV", "development").lower()
active_config: Config = ProductionConfig() if _env == "production" else DevelopmentConfig()
