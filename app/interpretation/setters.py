"""This module contains Classes for creating a boolean map for each Rotem
test category.

Classes: `ObstericSetter()`, `SurgerySetter()`, `CovidSetter()`,
`ResultFetcher()`.

"""
from typing import Literal
from typing import NamedTuple

from werkzeug.datastructures import ImmutableMultiDict

from app.interpretation.abc import CaseSetter
from app.interpretation.enums import RotemTests as RT
from app.interpretation.errors import Error
from app.interpretation.mappers import CovidMapper
from app.interpretation.mappers import ObstericMapper
from app.interpretation.mappers import SurgeryMapper


# ResultFetcher() exports to app.interpretation.__init__ for show_results()
__all__ = ("ResultFetcher",)


class ObstericSetter(CaseSetter):

    """ "Obsteric" Rotem test category values setter."""

    def __init__(self, row_data: ImmutableMultiDict):
        """Initialize `ObstericSetter` with an entered data.

        Initialize `ObstericMapper` as `self.case_mapper` to append `True`
        into `ObstericMapper.case_`<0|1|2|3|4|5|6|7|8> where number must
        be selected based on entered data.
        Call `self.handle()`

        """
        self.row_data = row_data
        self.case_mapper: ObstericMapper = ObstericMapper()

        # Debug
        self._case_mapper_name: str = self.case_mapper.__class__.__name__
        self._self_name: str = self.__class__.__name__

        # Run all
        self._result: str = self.handle()

    def _set(self) -> str:
        """Set values to corresponding value cases."""
        # Expected tuple where second value is int or float
        filtered: list[tuple[str, str]] = self.filter()

        # pass last cases if too big float value
        PASS_CASE = False
        for test_value in filtered:
            match test_value:

                # Too big bloat value handler
                case rt_any, value if rt_any in [
                    v for v in RT.__members__.values()
                ] and not value.isnumeric() and float(value) > 0.8:
                    self.case_mapper.case_0.append(True)
                    PASS_CASE = True

                case RT.EXTEM_CT, value if int(value) in range(40, 70):
                    self.case_mapper.case_1.append(True)
                case RT.EXTEM_CT, value if int(value) in range(80, 140):
                    self.case_mapper.case_5.append(True)
                    self.case_mapper.case_6.append(True)
                case RT.EXTEM_CT, value if int(value) in range(140, SurgerySetter.MAXSIZE):
                    self.case_mapper.case_6.append(True)

                case RT.EXTEM_A5, value if int(value) in range(25):
                    self.case_mapper.case_4.append(True)
                case RT.EXTEM_A5, value if int(value) in range(25, 35):
                    self.case_mapper.case_2.append(True)
                    self.case_mapper.case_3.append(True)
                case RT.EXTEM_A5, value if int(value) in range(35, SurgerySetter.MAXSIZE):
                    self.case_mapper.case_1.append(True)

                case RT.INTEM_CT, value if float(value) < 0.8:
                    self.case_mapper.case_7.append(True)
                case RT.INTEM_CT, value if int(value) in range(100, 240):
                    self.case_mapper.case_1.append(True)
                case RT.INTEM_CT, value if int(value) in range(240, SurgerySetter.MAXSIZE):
                    self.case_mapper.case_7.append(True)
                    self.case_mapper.case_8.append(True)

                case RT.FIBTEM_A5, value if int(value) in range(12):
                    self.case_mapper.case_2.append(True)
                    self.case_mapper.case_4.append(True)
                    self.case_mapper.case_6.append(True)
                case RT.FIBTEM_A5, value if int(value) in range(12, SurgerySetter.MAXSIsssZE):
                    self.case_mapper.case_1.append(True)
                    self.case_mapper.case_3.append(True)
                    self.case_mapper.case_5.append(True)

                case RT.HEPTEM_CT, value if float(value) < 0.8:
                    self.case_mapper.case_7.append(True)
                case RT.HEPTEM_CT, value if not PASS_CASE and int(value) in range(240):
                    self.case_mapper.case_7.append(True)
                case RT.HEPTEM_CT, value if not PASS_CASE and int(value) in range(240, SurgerySetter.MAXSIZE):
                    self.case_mapper.case_8.append(True)

                case _:
                    self.case_mapper.case_0.append(True)


class SurgerySetter(CaseSetter):

    """ "Surgery" Rotem test category values setter."""

    MAXSIZE: Literal = 1000

    def __init__(self, row_data: ImmutableMultiDict):
        """Initialize `SurgerySetter` with an entered data.

        Initialize `SurgerySetter` as `self.case_mapper` to append `True`
        into `ObstericMapper.case_`<0|1|2|3|4|5|6|7|8> where number must
        be selected based on entered data.
        Call `self.handle()`

        """
        self.row_data = row_data
        self.case_mapper: SurgeryMapper = SurgeryMapper()

        # Debug
        self._case_mapper_name: str = self.case_mapper.__class__.__name__
        self._self_name: str = self.__class__.__name__

        # Run all
        self._result: str = self.handle()

    def _set(self) -> str:
        """Set values to corresponding value cases."""
        # Expected tuple where second value is int or float
        filtered: list[tuple[str, str]] = self.filter()

        # pass last cases if too big float value
        PASS_CASE = False
        for test_value in filtered:
            match test_value:

                # Too big bloat value handler
                case rt_any, value if rt_any in [
                    v for v in RT.__members__.values()
                ] and not value.isnumeric() and float(value) > 0.8:
                    self.case_mapper.case_0.append(True)
                    PASS_CASE = True

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
                case RT.HEPTEM_CT, value if not PASS_CASE and int(value) in range(240):
                    self.case_mapper.case_3.append(True)
                case RT.HEPTEM_CT, value if not PASS_CASE and int(value) in range(240, SurgerySetter.MAXSIZE):
                    self.case_mapper.case_4.append(True)

                case _:
                    self.case_mapper.case_0.append(True)


class CovidSetter(CaseSetter):

    """ "Covid" Rotem test category values setter."""

    def __init__(self, row_data: ImmutableMultiDict):
        """Initialize `CovidSetter` with an entered data.

        Initialize `CovidSetter` as `self.case_mapper` to append `True`
        into `ObstericMapper.case_`<0|1|2|3|4|5|6|7|8> where number must
        be selected based on entered data.
        Call `self.handle()`

        """
        self.row_data = row_data
        self.case_mapper: CovidMapper = CovidMapper()

        # Debug
        self._case_mapper_name: str = self.case_mapper.__class__.__name__
        self._self_name: str = self.__class__.__name__

        # Run all
        self._result: str = self.handle()

    def _set(self) -> str:
        """Set values to corresponding value cases."""
        # Expected tuple where second value is int or float
        filtered: list[tuple[str, str]] = self.filter()

        for test_value in filtered:
            match test_value:

                case _:
                    self.case_mapper.case_0.append(True)


_Setter = ObstericSetter | SurgerySetter | CovidSetter


class ResultFetcher:

    """
    This class creates `ObstericSetter` | `SurgerySetter` | `CovidSetter`
    based on the Rotem test category.

    * No create an instance of itself.

    """

    def __new__(cls, entered_user_data: NamedTuple) -> _Setter:
        """Return `ObstericSetter`|`SurgerySetter`|`CovidSetter` instance."""
        return cls._match(entered_user_data)

    @staticmethod
    def _match(entered_user_data: NamedTuple) -> _Setter:
        """Fetch class by category, initialize and return its instance."""
        # session_data(str), request.form(ImmutableMultiDict) = EnteredUserData
        category, user_data = entered_user_data
        return {
            "obsteric_category": ObstericSetter(user_data),
            "surgery_category": SurgerySetter(user_data),
            "covid_category": CovidSetter(user_data),
            "session_error": Error.message("session_error"),
        }[category]
