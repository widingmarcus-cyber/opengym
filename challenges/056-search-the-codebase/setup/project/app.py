"""Main application entry point."""

from config import DEBUG, SECRET_KEY
from routes import (
    handle_get_users,
    handle_create_user,
    handle_get_posts,
    handle_create_post,
    handle_get_post_comments,
)


ROUTES = {
    "GET /users": handle_get_users,
    "POST /users": handle_create_user,
    "GET /posts": handle_get_posts,
    "POST /posts": handle_create_post,
    "GET /posts/comments": handle_get_post_comments,
}


def create_app():
    """Create and configure the application."""
    return {"routes": ROUTES, "debug": DEBUG}


def run():
    """Run the application."""
    app = create_app()
    print(f"Starting app with {len(app['routes'])} routes (debug={app['debug']})")


if __name__ == "__main__":
    run()
