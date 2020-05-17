from .auth_app import auth_blueprint
from .root_dir import blog_blueprint

__all__ = [
    "auth_blueprint",
    "blog_blueprint"
]