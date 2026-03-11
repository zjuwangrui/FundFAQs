"""Blueprint for comment-related endpoints."""

from flask import Blueprint, request

from config import active_config
from database import get_db
from utils import error_response, now_iso, paginate_args, paginated_response

comments_bp = Blueprint("comments", __name__)


# ---------------------------------------------------------------------------
# GET /api/articles/<article_id>/comments  –  list (paginated, newest first)
# ---------------------------------------------------------------------------

@comments_bp.route("", methods=["GET"])
def get_comments(article_id: int):
    page, per_page, offset = paginate_args(request, active_config.DEFAULT_COMMENT_PAGE_SIZE)

    with get_db() as conn:
        article = conn.execute(
            "SELECT id FROM articles WHERE id = ?", (article_id,)
        ).fetchone()
        if not article:
            return error_response("文章不存在", 404)

        total: int = conn.execute(
            "SELECT COUNT(*) FROM comments WHERE article_id = ?", (article_id,)
        ).fetchone()[0]
        rows = conn.execute(
            "SELECT * FROM comments WHERE article_id = ? "
            "ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (article_id, per_page, offset),
        ).fetchall()

    return paginated_response([dict(r) for r in rows], total, page, per_page, "comments")


def _require_admin_secret(data: dict):
    """Validate admin secret for protected operations."""
    secret = str(data.get("secret", "")).strip()
    if not secret:
        return error_response("缺少管理密钥", 403)
    if secret != active_config.ADMIN_SECRET:
        return error_response("管理密钥不正确", 403)
    return None


# ---------------------------------------------------------------------------
# POST /api/articles/<article_id>/comments  –  create (public)
# ---------------------------------------------------------------------------

@comments_bp.route("", methods=["POST"])
def create_comment(article_id: int):
    data = request.get_json(silent=True) or {}
    commenter = str(data.get("commenter", "")).strip() or "匿名"
    content = str(data.get("content", "")).strip()

    if not content:
        return error_response("评论内容不能为空")
    if len(content) > active_config.MAX_COMMENT_LENGTH:
        return error_response(f"评论内容不能超过 {active_config.MAX_COMMENT_LENGTH} 个字符")
    if len(commenter) > active_config.MAX_COMMENTER_LENGTH:
        return error_response(f"昵称不能超过 {active_config.MAX_COMMENTER_LENGTH} 个字符")

    with get_db() as conn:
        article = conn.execute(
            "SELECT id FROM articles WHERE id = ?", (article_id,)
        ).fetchone()
        if not article:
            return error_response("文章不存在", 404)

        cur = conn.execute(
            "INSERT INTO comments (article_id, commenter, content, created_at) VALUES (?, ?, ?, ?)",
            (article_id, commenter, content, now_iso()),
        )
        row = conn.execute(
            "SELECT * FROM comments WHERE id = ?", (cur.lastrowid,)
        ).fetchone()

    return dict(row), 201


# ---------------------------------------------------------------------------
# DELETE /api/articles/<article_id>/comments/<id>  –  delete (admin only)
# ---------------------------------------------------------------------------

@comments_bp.route("/<int:comment_id>", methods=["DELETE"])
def delete_comment(article_id: int, comment_id: int):
    data = request.get_json(silent=True) or {}

    # admin secret check
    err = _require_admin_secret(data)
    if err is not None:
        return err

    with get_db() as conn:
        cur = conn.execute(
            "DELETE FROM comments WHERE id = ? AND article_id = ?",
            (comment_id, article_id),
        )
        if cur.rowcount == 0:
            return error_response("评论不存在", 404)

    return {"message": "评论已删除"}
