"""This package contains interpretation-of-the-result functionality.

This module contains `EnteredUserData()` and `show_results()`.

"""
from typing import Literal
from typing import NamedTuple

from flask import session
from werkzeug.datastructures import ImmutableMultiDict

from app.interpretation.mappers import json_dumps_ru
from app.interpretation.setters import ResultFetcher


# show_results() exports to app.views.menu for results_interpretation() view
__all__ = ("show_results",)


class EnteredUserData(NamedTuple):

    """Contains clicked-test-category-button-name and POST data."""

    category: Literal["obsteric_category"] | Literal["surgery_category"] | Literal["covid_category"]
    user_data: ImmutableMultiDict
    # Example user_data:
    # ImmutableMultiDict([
    #     ('data_extem_ct', '1'),
    #     ('data_extem_a5', '0.8'),
    #     ('data_intem_ct', ''),
    #     ('data_fibtem_a5', ''),
    #     ('data_heptem_ct', '')
    # ])

    def __repr__(self) -> str:
        return f"{type(self).__name__}(category={self.category!r}, user_data={self.user_data!r})"


def show_results(entered_data: ImmutableMultiDict) -> str:
    """Return interpretation of the result.

    Init `EnteredUserData()` with `session["clicked_category_button"]`
    and `entered_data`.

    """
    session_data: str = session.get("clicked_category_button", "session_error")
    entered: EnteredUserData = EnteredUserData(session_data, entered_data)
    return json_dumps_ru(ResultFetcher(entered), default=vars)
