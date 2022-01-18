"""This module contains objects for creating a boolean map for each test
category.

"""
from typing import Literal
from typing import NamedTuple

from werkzeug.datastructures import ImmutableMultiDict

from app.interpretation.abc import CaseSetter
from app.interpretation.enums import RotemTests as RT
from app.interpretation.errors import Error
from app.interpretation.mappers import CovidMapper
from app.interpretation.mappers import ObstericsMapper
from app.interpretation.mappers import SurgeryMapper


__all__ = ("ResultFetcher",)


class ObstericSetter(CaseSetter):

    """This class to set set values for "Obsteric" test category."""

    def __init__(self, row_data) -> None:
        self.row_data = row_data
        self.case_mapper = ObstericsMapper()

    def _set(self):
        pass

    def filter(self):
        pass

    @property
    def interpret_result(self):
        pass


class SurgerySetter(CaseSetter):

    """This class to set set values for "Surgery" test category."""

    MAXSIZE: Literal = 1000

    def __init__(self, row_data):
        """Initialize `SurgerySetter` with an entered data.

        Initialize `SurgeryMapper` as `self.case_mapper` to
        `SurgeryMapper.case_`<0|1|2|3|4|5|6|7|8>`.append(True)` where
        number must be selected (in `self.map()`) based on user input.

        """
        self.row_data = row_data
        self.case_mapper = SurgeryMapper()
        self._result: str = self.interpret_result

    def _set(self) -> str:
        """Set values to corresponding value cases."""
        filled_user_data = self.filter()
        for filled_input_form_field in filled_user_data:
            match filled_input_form_field:

                case RT.EXTEM_CT, value if int(value) in range(40, 80):
                    self.case_mapper.case_1.append(True)
                    self.case_mapper.case_3.append(True)
                case RT.EXTEM_CT, value if int(value) in range(80, SurgerySetter.MAXSIZE):
                    self.case_mapper.case_2.append(True)

                case RT.EXTEM_A5, value if int(value) in range(25):
                    self.case_mapper.case_7.append(True)
                    self.case_mapper.case_8.append(True)
                case RT.EXTEM_A5, value if int(value) in range(25, 35):
                    self.case_mapper.case_5.append(True)
                    self.case_mapper.case_7.append(True)
                case RT.EXTEM_A5, value if int(value) in range(37, SurgerySetter.MAXSIZE):
                    self.case_mapper.case_1.append(True)

                case RT.INTEM_CT, value if float(value) < 0.8:
                    self.case_mapper.case_3.append(True)
                case RT.INTEM_CT, value if int(value) in range(100, 240):
                    self.case_mapper.case_1.append(True)
                case RT.INTEM_CT, value if int(value) in range(240, SurgerySetter.MAXSIZE):
                    self.case_mapper.case_3.append(True)
                    self.case_mapper.case_4.append(True)

                case RT.FIBTEM_A5, value if int(value) in range(8):
                    self.case_mapper.case_5.append(True)
                    self.case_mapper.case_8.append(True)
                case RT.FIBTEM_A5, value if int(value) in range(8, SurgerySetter.MAXSIZE):
                    self.case_mapper.case_1.append(True)
                    self.case_mapper.case_2.append(True)
                    self.case_mapper.case_7.append(True)

                case RT.HEPTEM_CT, value if float(value) < 0.8:
                    self.case_mapper.case_3.append(True)
                case RT.HEPTEM_CT, value if int(value) in range(240):
                    self.case_mapper.case_3.append(True)
                case RT.HEPTEM_CT, value if int(value) in range(240, SurgerySetter.MAXSIZE):
                    self.case_mapper.case_4.append(True)

                case _:
                    self.case_mapper.case_0.append(True)

    def filter(self) -> list[tuple[str, str]]:
        """Filter fields as (name, value) in which data entered."""
        return [(name, value) for name, value in self.row_data.items() if value]

    @property
    def interpret_result(self) -> str:
        """Set values to corresponding value cases and return rusult."""
        self._set()
        result: dict = self.case_mapper.match_case()
        return str(result)


class CovidSetter(CaseSetter):

    """This class to set set values for "Covid" test category."""

    def __init__(self, row_data: ImmutableMultiDict):
        """Initialize `CovidSetter` with an entered data.

        Initialize `CovidMapper` as `self.case_mapper` to
        `CovidMapper.case_<0|1|2>.append(True)` where number
        must be selected (in `self.map()`) based on user input.

        """
        self.row_data = row_data
        self.case_mapper = CovidMapper()
        self._result: str = self.interpret_result

    def _set(self) -> str:
        """
        Match the Rotem-test-name and range of valid values
        to the corresponding caseto append `True`.

        """
        filled_user_data = self.filter()
        for filled_input_form_field in filled_user_data:
            match filled_input_form_field:

                case _:
                    self.case_mapper.case_0.append(True)

    def filter(self) -> list[tuple[str, str]]:
        """Filter fields as (name, value) in which data entered."""
        return [(name, value) for name, value in self.row_data.items() if value]

    @property
    def interpret_result(self) -> str:
        """Set values to corresponding value cases and return rusult."""
        self._set()
        result: dict = self.case_mapper.match_case()
        return str(result)


_Setter = ObstericSetter | SurgerySetter | CovidSetter


class ResultFetcher:

    """
    This class create `ObstericSetter` | `SurgerySetter` | `CovidSetter`
    based on the test category.

    * No create an instance of itself.

    """

    def __new__(cls, entered_user_data: NamedTuple) -> _Setter:
        """Return `ObstericSetter`|`SurgerySetter`|`CovidSetter` instance."""
        return cls._parse(entered_user_data)

    @staticmethod
    def _parse(entered_user_data: NamedTuple) -> _Setter:
        """Fetch class by test category, create and return its instance.
        `entered_user_data` has tuple(test category, user data).

        """
        category, user_data = entered_user_data
        return {
            "obsteric_category": ObstericSetter(user_data),
            "surgery_category": SurgerySetter(user_data),
            "covid_category": CovidSetter(user_data),
            "session_error": Error.message("session_error"),
        }[category]
