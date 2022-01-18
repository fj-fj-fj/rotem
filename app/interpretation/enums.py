"""This module contains enums."""
from enum import Enum

from app.custom_types import frozendict


__all__ = ("RotemTests", "SurgeryInterpetation")


class RotemTests(str, Enum):

    """Rotem tests: EXTEM, INTEM, FIBTEM, HEPTEM, NATEM, NAHERTEM."""

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
    NAHERTEM_CT = "data_naheptem_ct"


class SurgeryInterpetation(dict, Enum):

    """Bleeding correction tactics for surgery tests."""

    HEMOSTASIS_CORRECTION_IS_NOT_SHOWN = frozendict(
        {
            "title": "Коррекция гемостаза не показана",
            "description": "При коровотечении акцент на хирургический гемостаз",
        }
    )
    DEFICIENCY_OF_FACTORS_EXTERNALLY = frozendict(
        {
            "title": "Дефицит факторов внешнего пути",
            "description": (
                "(Ауто)плазма 10-15 мл/кг или\n"
                "Концентрат протромбинового комплекса (Протромплекс, Октаплекс)\n"
                "CT EXTEM 81-100 сек - 7,5 МЕ/кг\n"
                "CT EXTEM 101-120 сек - 15 МЕ/кг\n"
                "CT EXTEM >120 сек – 22,5 МЕ/кг"
            ),
        }
    )
    HEPARIN_EFFECT = frozendict(
        {
            "title": "Эффект гепарина",
            "description": "Протамин 0,25-0,5 мг/кг",
        }
    )
    DEFICIENCY_OF_FACTORS_INTERNALLY = frozendict(
        {
            "title": "Дефицит факторов внутреннего пути",
            "description": "(Ауто)плазма 10-15 мл/кг",
        }
    )
    FIBRINOGEN_DEFICIENCY = frozendict(
        {
            "title": "Дефицит фибриногена",
            "description": "Криопреципитат до достижения FIBTEM A5 10 мм (см. расчет дозы)",
        }
    )
    HIPERFIBRINOLYSIS = frozendict(
        {
            "title": "Гиперфибринолиз",
            "description": ("Транексам/ЭАКК\n" "При признаках гипофибриногенемии - криопреципитат в расчетной дозе"),
        }
    )
    SIGNIFICIANT_THROMBOCYTOPENIA = frozendict(
        {
            "title": "Значимая тромбоцитопения",
            "description": "Тромбоцитный концентрат",
        }
    )
    FIBRINOGEN_DEFICIENCY_AND_SIGNIFICIANT_THROMBOCYTOPENIA = frozendict(
        {
            "title": "Дефицит фибриногена и значимая тромбоцитопения",
            "description": (
                "Криопреципитат до достижения FIBTEM A5 10 мм (см. расчет дозы)\n" "Тромбоцитный концентрат"
            ),
        }
    )


class LowMoleuclarWeightHeparin(float, Enum):

    """Low-molecular-weight [LMWH] heparin doses."""

    ZERO_ZERO = 0.0
    ZERO_ONE = 0.1
    ZERO_TWO = 0.2
    ZERO_SIX = 0.6
    ZERO_EIGHT = 0.8
    ONE_TWO = 1.2
    ONT_SIX = 1.6


class UnfractionatedHeparin(float, Enum):

    """Unfractionated heparin [UH] doses."""

    ZERO_ZERO = 0.0
    ZERO_ONE = 0.1
    ZERO_TWO = 0.2
    ZERO_SIX = 0.6
    ZERO_EIGHT = 0.8
