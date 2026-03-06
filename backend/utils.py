"""Shared utility helpers used across route modules."""

import datetime

from flask import jsonify
from typing import Any


def now_iso() -> str:
    """Return the current UTC time as an ISO-8601 string (seconds precision)."""
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")


def paginate_args(request, default_per_page: int = 10) -> tuple[int, int, int]:
    """
    Extract and validate pagination query parameters from *request*.

    Returns:
        (page, per_page, offset)  – all guaranteed to be sane integers.
    """
    from config import active_config

    page = max(request.args.get("page", 1, type=int), 1)
    per_page = min(
        max(request.args.get("per_page", default_per_page, type=int), 1),
        active_config.MAX_PAGE_SIZE,
    )
    offset = (page - 1) * per_page
    return page, per_page, offset


def paginated_response(items: list[Any], total: int, page: int, per_page: int, key: str) -> Any:
    """Build a standard paginated JSON response."""
    total_pages = max((total + per_page - 1) // per_page, 1)
    return jsonify(
        {
            key: items,
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages,
        }
    )


def error_response(message: str, status: int = 400):
    """Return a JSON error envelope with *status* HTTP code."""
    return jsonify({"error": message}), status
