import json
from enum import Enum
from collections.abc import Mapping
from typing import Callable, Literal

from werkzeug.datastructures import ImmutableMultiDict


def json_dumps_ru(interpretation_data: Mapping, default: Callable | None = None) -> str:
    """`json.dumps with `ensure_ascii=False`.

    Return value can contain non-ASCII characters if they appear in strings
    contained in obj. Otherwise, all such characters are escaped in JSON strings.
    """
    return json.dumps(interpretation_data, ensure_ascii=False, default=default)


class Rotem(str, Enum):
    """Rotem tests: EXTEM, INTEM, FIBTEM, HEPTEM, NATEM. (Also CSS classes ;)"""

    EXTEM_CT = "data_extem_ct"
    EXTEM_A5 = "data_extem_a5"
    INTEM_CT = "data_intem_ct"
    INTEM_A5 = "data_intem_a5"
    FIBTEM_CT = "data_fibtem_ct"
    FIBTEM_A5 = "data_fibtem_a5"
    HEPTEM_CT = "data_heptem_ct"
    HEPTEM_A5 = "data_heptem_a5"
    NATEM_CT = "data_natem_ct"
    NATEM_A5 = "data_natem_a5"


class BleedingCorrectionTactics(dict, Enum):
    """Interpretations of results (Rotem tests)."""

    HEMOSTASIS_CORRECTION_IS_NOT_SHOWN = {
        "title": "Коррекция гемостаза не показана",
        "description": "При коровотечении акцент на хирургический гемостаз",
    }
    DEFICIENCY_OF_FACTORS_EXTERNALLY = {
        "title": "Дефицит факторов внешнего пути",
        "description": (
            "(Ауто)плазма 10-15 мл/кг или\n"
            "Концентрат протромбинового комплекса (Протромплекс, Октаплекс)\n"
            "CT EXTEM 81-100 сек - 7,5 МЕ/кг\n"
            "CT EXTEM 101-120 сек - 15 МЕ/кг\n"
            "CT EXTEM >120 сек – 22,5 МЕ/кг"
        ),
    }
    HEPARIN_EFFECT = {
        "title": "Эффект гепарина",
        "description": "Протамин 0,25-0,5 мг/кг",
    }
    DEFICIENCY_OF_FACTORS_INTERNALLY = {
        "title": "Дефицит факторов внутреннего пути",
        "description": "(Ауто)плазма 10-15 мл/кг",
    }
    FIBRINOGEN_DEFICIENCY = {
        "title": "Дефицит фибриногена",
        "description": "Криопреципитат до достижения FIBTEM A5 10 мм (см. расчет дозы)"
    }
    HIPERFIBRINOLYSIS = {
        "title": "Гиперфибринолиз",
        "description": (
            "Транексам/ЭАКК\n"
            "При признаках гипофибриногенемии - криопреципитат в расчетной дозе"
        ),
    }
    SIGNIFICIANT_THROMBOCYTOPENIA = {
        "title": "Значимая тромбоцитопения",
        "description": "Тромбоцитный концентрат",
    }
    FIBRINOGEN_DEFICIENCY_AND_SIGNIFICIANT_THROMBOCYTOPENIA = {
        "title": "Дефицит фибриногена и значимая тромбоцитопения",
        "description": (
            "Криопреципитат до достижения FIBTEM A5 10 мм (см. расчет дозы)\n"
            "Тромбоцитный концентрат"
        ),
    }


class CaseMapper:
    """
    Class for creating boolean lists of entered user data and
    search for relevant interpretation based on this lists.
    The process of creating lists and searching for the result
    see in `ResultInterpreter.map()`.
    """

    def __init__(self):
        self.case_0 = []
        self.case_1 = []
        self.case_2 = []
        self.case_3 = []
        self.case_4 = []
        self.case_5 = []
        self.case_6 = []
        self.case_7 = []
        self.case_8 = []

    def search_case(self) -> str:
        """Find case for entered data and return its interpretation."""
        for _case in vars(self).items():
            match _case:
                case "case_1", [True, True, True, True]:
                    return json_dumps_ru(BleedingCorrectionTactics.HEMOSTASIS_CORRECTION_IS_NOT_SHOWN)
                case "case_2", [True, True]:
                    return json_dumps_ru(BleedingCorrectionTactics.DEFICIENCY_OF_FACTORS_EXTERNALLY)
                case "case_3", [True, True]:
                    return json_dumps_ru(BleedingCorrectionTactics.HEPARIN_EFFECT)
                case "case_4", [True, True]:
                    return json_dumps_ru(BleedingCorrectionTactics.DEFICIENCY_OF_FACTORS_INTERNALLY)
                case "case_5", [True, True]:
                    return json_dumps_ru(BleedingCorrectionTactics.FIBRINOGEN_DEFICIENCY)
                # FIXME: Об этом случае нам нужно поговорить
                # case "case_6", [True, True, True, True]:
                #     return json_dumps_ru(BleedingCorrectionTactics.HIPERFIBRINOLYSIS)
                case "case_7", [True, True]:
                    return json_dumps_ru(BleedingCorrectionTactics.SIGNIFICIANT_THROMBOCYTOPENIA)
                case "case_8", [True, True]:
                    return json_dumps_ru(
                        BleedingCorrectionTactics.FIBRINOGEN_DEFICIENCY_AND_SIGNIFICIANT_THROMBOCYTOPENIA
                    )
                case _:
                    bad_data_error_message = {
                        "error": "bad_data_error",
                        "title": "Что-то тут не так!",
                        "description": "Проверьте еще раз свои данные",
                    }
        return json_dumps_ru(bad_data_error_message)

    def __repr__(self):
        return f"{self.__class__.__name__}({vars(self)})"


class ResultInterpreter:

    MAXSIZE: Literal = 1000

    def __init__(self, row_data: ImmutableMultiDict):
        self.row_data = row_data
        self.case_mapper = CaseMapper()
        self.result: str = self.map()

    def map(self) -> str:
        """
        Match the Potem test name(str) and range of valid vaules(int)
        to the corresponding case(list) to append `True`.
        """
        filled_user_data = self.filter()
        for filled_input_form_field in filled_user_data:
            match filled_input_form_field:

                case Rotem.EXTEM_CT, value if int(value) in range(40, 80):
                    self.case_mapper.case_1.append(True)
                    self.case_mapper.case_3.append(True)
                case Rotem.EXTEM_CT, value if int(value) in range(80, ResultInterpreter.MAXSIZE):
                    self.case_mapper.case_2.append(True)

                case Rotem.EXTEM_A5, value if int(value) in range(25):
                    self.case_mapper.case_7.append(True)
                    self.case_mapper.case_8.append(True)
                case Rotem.EXTEM_A5, value if int(value) in range(25, 35):
                    self.case_mapper.case_5.append(True)
                    self.case_mapper.case_7.append(True)
                case Rotem.EXTEM_A5, value if int(value) in range(37, ResultInterpreter.MAXSIZE):
                    self.case_mapper.case_1.append(True)

                case Rotem.INTEM_CT, value if float(value) < .8:
                    self.case_mapper.case_3.append(True)
                case Rotem.INTEM_CT, value if int(value) in range(100, 240):
                    self.case_mapper.case_1.append(True)
                case Rotem.INTEM_CT, value if int(value) in range(240, ResultInterpreter.MAXSIZE):
                    self.case_mapper.case_3.append(True)
                    self.case_mapper.case_4.append(True)

                case Rotem.FIBTEM_A5, value if int(value) in range(8):
                    self.case_mapper.case_5.append(True)
                    self.case_mapper.case_8.append(True)
                case Rotem.FIBTEM_A5, value if int(value) in range(8, ResultInterpreter.MAXSIZE):
                    self.case_mapper.case_1.append(True)
                    self.case_mapper.case_2.append(True)
                    self.case_mapper.case_7.append(True)

                case Rotem.HEPTEM_CT, value if float(value) < .8:
                    self.case_mapper.case_3.append(True)
                case Rotem.HEPTEM_CT, value if int(value) in range(240):
                    self.case_mapper.case_3.append(True)
                case Rotem.HEPTEM_CT, value if int(value) in range(240, ResultInterpreter.MAXSIZE):
                    self.case_mapper.case_4.append(True)

                # FIXME: Об этом случае нам нужно поговорить
                # case ?:
                #     self.case_mapper.case_6.append(True)

                case _:
                    self.case_mapper.case_0.append(True)

        result: dict = self.case_mapper.search_case()
        return str(result)

    def filter(self) -> list[tuple[str, str]]:
        """Filter fields as (name, value) in which data entered."""
        return [(name, value) for name, value in self.row_data.items() if value]

    def __repr__(self):
        return f"{self.__class__.__name__}({self.row_data!r})"

    def __str__(self):
        """Return interpretation of results."""
        return self.result


def show_results(post_form_data: ImmutableMultiDict) -> str:
    return json_dumps_ru(ResultInterpreter(post_form_data), default=vars)
