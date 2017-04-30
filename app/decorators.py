"""
权限检查
"""

from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission


def permission_required(permission):
    def decorators(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(404)
            return func(*args, **kwargs)

        return decorated_function
    return decorators


def admin_required(func):
    return permission_required(Permission.ADMINISTER)(func)

