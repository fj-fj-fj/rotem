"""Module contains "breadcrumb" functional."""
from collections import namedtuple
from functools import wraps
from typing import Callable

from flask import g
from flask import request


# register_breadcrumb() exports to app.interpretation.views{menu,routes}
__all__ = ("register_breadcrumb",)

_BreadCrumb = namedtuple("_BreadCrumb", ["path", "title"])


def register_breadcrumb(view_title: str, aside_menu: bool = False) -> Callable:
    """Decorator to create breadcrumbs."""

    def decorator(funk: Callable) -> Callable:
        @wraps(funk)
        def decorated_function(*args, **kwargs):
            # Set page title
            g.title = view_title.capitalize()
            g.breadcrumbs = []
            if aside_menu:
                g.breadcrumbs.append(_BreadCrumb("#", "меню"))
            g.breadcrumbs.append(_BreadCrumb(request.path, view_title))

            return funk(*args, **kwargs)

        return decorated_function

    return decorator
