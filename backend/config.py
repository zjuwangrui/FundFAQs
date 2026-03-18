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

    # Email Configuration
    # 这里存储用来【发送邮件】的 SMTP 服务器配置（仅需配置一个账号）
    MAIL_SERVER: str = "smtp.qq.com"
    MAIL_PORT: int = 465
    MAIL_USE_TLS: bool = False
    
    # 发件人账号与授权码
    MAIL_USERNAME: str = "1960881478@qq.com"
    MAIL_PASSWORD: str = "gkeegnifbncwjecc"
    
    # 默认发件人显示
    MAIL_DEFAULT_SENDER: str = "FundFAQs <1960881478@qq.com>"
    
    # 接收通知的管理员邮箱列表 (以逗号分隔，可包含任意邮箱)
    ADMIN_EMAILS: str = "1960881478@qq.com,17382016364@163.com"

    # CORS – in production restrict to actual frontend origin

    # CORS – in production restrict to actual frontend origin
    CORS_ORIGINS: str = "*"

    # Admin secret for protected article operations (update/delete).
    # In production, override via environment variable FUNDFAQ_ADMIN_SECRET.
    ADMIN_SECRET: str = os.getenv("FUNDFAQ_ADMIN_SECRET", "zizhumail")


class DevelopmentConfig(Config):
    DEBUG: bool = True


class ProductionConfig(Config):
    DEBUG: bool = False


# Active configuration resolved from environment variable
_env = os.getenv("FLASK_ENV", "development").lower()
active_config: Config = ProductionConfig() if _env == "production" else DevelopmentConfig()
