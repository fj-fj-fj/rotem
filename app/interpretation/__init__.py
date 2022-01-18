"""This package contains interpretation-of-the result functionality."""
from typing import NamedTuple

from flask import session
from werkzeug.datastructures import ImmutableMultiDict

from app.interpretation.mappers import json_dumps_ru
from app.interpretation.setters import ResultFetcher


__all__ = ("show_results",)


class EnteredUserData(NamedTuple):
    """Contains clicked test-category-button-name and POST data."""

    category: str
    user_data: ImmutableMultiDict

    def __repr__(self) -> str:
        return f"<EnteredUserData {self.category!r}, {self.user_data!r}>"


def show_results(entered_data: ImmutableMultiDict) -> str:
    """Return interpretation of the result."""
    session_data: str = session.get("clicked_category_button", "session_error")
    entered = EnteredUserData(session_data, entered_data)
    return json_dumps_ru(ResultFetcher(entered), default=vars)
