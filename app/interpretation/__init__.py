"""This package contains interpretation-of-the-result functionality.

This module contains `EnteredUserData()` and `show_results()`.

"""
from typing import Literal
from typing import NamedTuple

from flask import session
from werkzeug.datastructures import ImmutableMultiDict

from app.interpretation.setters import ResultFetcher
from app.interpretation.utils import json_dumps_ru


# show_results() exports to app.views.menu for results_interpretation() view
__all__ = ("show_results",)

# https://SITE/interpretation-of-results page has three buttons.
# Depending on the selected category, a form will be displayed.
# Java Script sends information about the pressed button to the
# server side. `app.views.menu.results_interpretation()` sets
# client side data to the session as 'clicked_category_button'.
_CATEGORY_TYPE = Literal["obsteric_category"] | Literal["surgery_category"] | Literal["covid_category"]
# This will be used to select setters to build the boolean map
# (see app.interpretation.setters) and mappers to get the desired
# case (see app.interpretation.mappers).


class EnteredUserData(NamedTuple):

    """Contains clicked-test-category-button-name and POST data."""

    category: _CATEGORY_TYPE
    # category example: 'obsteric_category'
    user_data: ImmutableMultiDict
    # user_data example:
    # ImmutableMultiDict([
    #     ('data_extem_ct', '1'),
    #     ('data_extem_a5', '0.8'),
    #     ('data_intem_ct', ''),
    #     ('data_fibtem_a5', ''),
    #     ('data_heptem_ct', '')
    # ])

    def __repr__(self) -> str:
        """Return class name with `category` and `user_data`."""
        return f"{type(self).__name__}(category={self.category!r}, user_data={self.user_data!r})"


def show_results(entered_data: ImmutableMultiDict) -> str:
    """Return interpretation of the result.

    Init `EnteredUserData()` with `session["clicked_category_button"]`
    and `entered_data`.

    """
    # Fetch category type from session
    clicked: _CATEGORY_TYPE = session.get("clicked_category_button", "session_error")
    # Initialize `EnteredUserData` with fetched category type and input data
    entered: EnteredUserData = EnteredUserData(clicked, entered_data)
    # Initialize `ResultFetcher` with `EnteredUserData` instance
    # Return interpretation of the result or error (see app.interpretation.setters)
    return json_dumps_ru(ResultFetcher(entered), default=vars)
