"""Route handlers for the web application."""

from models import User, Post, Comment
from database import get_db
from utils import validate_email, hash_password, format_response, paginate


def handle_get_users(request):
    """Handle GET /users request."""
    db = get_db()
    db.connect()
    users = db.execute_query("SELECT * FROM users")
    db.disconnect()
    return format_response(users)


def handle_create_user(request):
    """Handle POST /users request."""
    email = request.get("email", "")
    if not validate_email(email):
        return format_response(None, status="error")
    user = User(None, request["username"], email)
    return format_response(user.to_dict())


def handle_get_posts(request):
    """Handle GET /posts request."""
    page = request.get("page", 1)
    db = get_db()
    db.connect()
    posts = db.execute_query("SELECT * FROM posts")
    db.disconnect()
    return format_response(paginate(posts, page, 10))


def handle_create_post(request):
    """Handle POST /posts request."""
    post = Post(None, request["title"], request["content"], request["author_id"])
    return format_response(post.to_dict())


def handle_get_post_comments(request):
    """Handle GET /posts/:id/comments request."""
    db = get_db()
    db.connect()
    comments = db.execute_query("SELECT * FROM comments WHERE post_id = ?")
    db.disconnect()
    return format_response(comments)
