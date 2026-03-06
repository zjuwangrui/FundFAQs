"""Blueprint for article-related endpoints."""

from flask import Blueprint, request

from config import active_config
from database import get_db
from utils import error_response, now_iso, paginate_args, paginated_response

articles_bp = Blueprint("articles", __name__)


# ---------------------------------------------------------------------------
# GET /api/articles  –  list (paginated)
# ---------------------------------------------------------------------------

@articles_bp.route("", methods=["GET"])
def get_articles():
    page, per_page, offset = paginate_args(request, active_config.DEFAULT_PAGE_SIZE)

    with get_db() as conn:
        total: int = conn.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
        rows = conn.execute(
            "SELECT id, title, content, created_at, updated_at "
            "FROM articles ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (per_page, offset),
        ).fetchall()

    return paginated_response([dict(r) for r in rows], total, page, per_page, "articles")


# ---------------------------------------------------------------------------
# GET /api/articles/search  –  full-text search
# ---------------------------------------------------------------------------

@articles_bp.route("/search", methods=["GET"])
def search_articles():
    q = request.args.get("q", "").strip()
    page, per_page, offset = paginate_args(request, active_config.DEFAULT_PAGE_SIZE)

    if not q:
        return paginated_response([], 0, 1, per_page, "articles")

    like_q = f"%{q}%"
    with get_db() as conn:
        total: int = conn.execute(
            "SELECT COUNT(*) FROM articles WHERE title LIKE ? OR content LIKE ?",
            (like_q, like_q),
        ).fetchone()[0]
        rows = conn.execute(
            "SELECT id, title, content, created_at, updated_at "
            "FROM articles WHERE title LIKE ? OR content LIKE ? "
            "ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (like_q, like_q, per_page, offset),
        ).fetchall()

    return paginated_response([dict(r) for r in rows], total, page, per_page, "articles")


# ---------------------------------------------------------------------------
# GET /api/articles/<id>  –  single article
# ---------------------------------------------------------------------------

@articles_bp.route("/<int:article_id>", methods=["GET"])
def get_article(article_id: int):
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM articles WHERE id = ?", (article_id,)
        ).fetchone()

    if not row:
        return error_response("文章不存在", 404)
    return dict(row)   # Flask 3 auto-jsonifies dicts


# ---------------------------------------------------------------------------
# POST /api/articles  –  create
# ---------------------------------------------------------------------------

@articles_bp.route("", methods=["POST"])
def create_article():
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    content = str(data.get("content", "")).strip()

    if not title:
        return error_response("标题不能为空")
    if not content:
        return error_response("内容不能为空")
    if len(title) > active_config.MAX_TITLE_LENGTH:
        return error_response(f"标题不能超过 {active_config.MAX_TITLE_LENGTH} 个字符")

    ts = now_iso()
    with get_db() as conn:
        cur = conn.execute(
            "INSERT INTO articles (title, content, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (title, content, ts, ts),
        )
        row = conn.execute(
            "SELECT * FROM articles WHERE id = ?", (cur.lastrowid,)
        ).fetchone()

    return dict(row), 201


# ---------------------------------------------------------------------------
# PUT /api/articles/<id>  –  update
# ---------------------------------------------------------------------------

@articles_bp.route("/<int:article_id>", methods=["PUT"])
def update_article(article_id: int):
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    content = str(data.get("content", "")).strip()

    if not title:
        return error_response("标题不能为空")
    if not content:
        return error_response("内容不能为空")
    if len(title) > active_config.MAX_TITLE_LENGTH:
        return error_response(f"标题不能超过 {active_config.MAX_TITLE_LENGTH} 个字符")

    ts = now_iso()
    with get_db() as conn:
        conn.execute(
            "UPDATE articles SET title = ?, content = ?, updated_at = ? WHERE id = ?",
            (title, content, ts, article_id),
        )
        row = conn.execute(
            "SELECT * FROM articles WHERE id = ?", (article_id,)
        ).fetchone()

    if not row:
        return error_response("文章不存在", 404)
    return dict(row)
