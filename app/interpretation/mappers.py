"""This module contains objects for fetching 'interpretation of the result'
by a boolean maps.

"""
from app.interpretation.abc import CaseMapper
from app.interpretation.enums import ObstericInterpetation as OI
from app.interpretation.enums import SurgeryInterpetation as SI
from app.interpretation.errors import Error
from app.interpretation.utils import json_dumps_ru


__all__ = "CovidMapper", "ObstericMapper", "SurgeryMapper"


class ObstericMapper(CaseMapper):

    """Class for mapping relevant interpretation for "obsterics" tests."""

    def __init__(self):
        """Initialize `ObstericMapper` with boolean lists of entered data."""
        self.case_0 = []  # Error case
        self.case_1 = []  # HEMOSTASIS_CORRECTION_IS_NOT_SHOWN case
        self.case_2 = []  # FIBRINOGEN_DEFICIENCY case
        self.case_3 = []  # SIGNIFICIANT_THROMBOCYTOPENIA case
        self.case_4 = []  # FIBRINOGEN_DEFICIENCY_AND_SIGNIFICIANT_THROMBOCYTOPENIA case
        self.case_5 = []  # DEFICIENCY_OF_FACTORS_EXTERNALLY case
        self.case_6 = []  # FIBRINOGEN_DEFICIENCY_POSSIBLE_AND_DEFICIENCY_OF_EXTRINSIC_PATHWAY_FACTORS case
        self.case_7 = []  # HEPARIN_EFFECT case
        self.case_8 = []  # DEFICIENCY_OF_FACTORS_INTERNALLY case

    def match_case(self) -> str:
        """Return an interpretation of the results by the correct combination
        of values or an error if no case matches.

        """
        for _case in vars(self).items():
            match _case:
                case "case_1", [True, True, True, True]:
                    return json_dumps_ru(OI.HEMOSTASIS_CORRECTION_IS_NOT_SHOWN)
                case "case_2", [True, True]:
                    return json_dumps_ru(OI.FIBRINOGEN_DEFICIENCY)
                case "case_3", [True, True]:
                    return json_dumps_ru(OI.SIGNIFICIANT_THROMBOCYTOPENIA)
                case "case_4", [True, True]:
                    return json_dumps_ru(OI.FIBRINOGEN_DEFICIENCY_AND_SIGNIFICIANT_THROMBOCYTOPENIA)
                case "case_5", [True, True]:
                    return json_dumps_ru(OI.DEFICIENCY_OF_FACTORS_EXTERNALLY)
                case "case_6", [True, True]:
                    return json_dumps_ru(OI.FIBRINOGEN_DEFICIENCY_POSSIBLE_AND_DEFICIENCY_OF_EXTRINSIC_PATHWAY_FACTORS)
                case "case_7", [True, True]:
                    return json_dumps_ru(OI.HEPARIN_EFFECT)
                case "case_8", [True, True]:
                    return json_dumps_ru(OI.DEFICIENCY_OF_FACTORS_INTERNALLY)
                case _:  # case_0 or other
                    BAD_DATA_ERROR_MESSAGE: dict = Error.message("map_error")
        return json_dumps_ru(BAD_DATA_ERROR_MESSAGE)  # type: ignore


class SurgeryMapper(CaseMapper):

    """Class for mapping relevant interpretation for "surgey" tests."""

    def __init__(self):
        """Initialize `SurgeryMapper` with boolean lists of entered data."""
        self.case_0 = []  # Error case
        self.case_1 = []  # HEMOSTASIS_CORRECTION_IS_NOT_SHOWN case
        self.case_2 = []  # DEFICIENCY_OF_FACTORS_EXTERNALLY case
        self.case_3 = []  # HEPARIN_EFFECT case
        self.case_4 = []  # DEFICIENCY_OF_FACTORS_INTERNALLY case
        self.case_5 = []  # FIBRINOGEN_DEFICIENCY case
        self.case_6 = []  # HIPERFIBRINOLYSIS case
        self.case_7 = []  # SIGNIFICIANT_THROMBOCYTOPENIA case
        self.case_8 = []  # FIBRINOGEN_DEFICIENCY_AND_SIGNIFICIANT_THROMBOCYTOPENIA case

    def match_case(self) -> str:
        """Return an interpretation of the result by the correct combination
        of values or an error if no case matches.

        """
        for _case in vars(self).items():
            match _case:
                case "case_1", [True, True, True, True]:
                    return json_dumps_ru(SI.HEMOSTASIS_CORRECTION_IS_NOT_SHOWN)
                case "case_2", [True, True]:
                    return json_dumps_ru(SI.DEFICIENCY_OF_FACTORS_EXTERNALLY)
                case "case_3", [True, True]:
                    return json_dumps_ru(SI.HEPARIN_EFFECT)
                case "case_4", [True, True]:
                    return json_dumps_ru(SI.DEFICIENCY_OF_FACTORS_INTERNALLY)
                case "case_5", [True, True]:
                    return json_dumps_ru(SI.FIBRINOGEN_DEFICIENCY)
                case "case_7", [True, True]:
                    return json_dumps_ru(SI.SIGNIFICIANT_THROMBOCYTOPENIA)
                case "case_8", [True, True]:
                    return json_dumps_ru(SI.FIBRINOGEN_DEFICIENCY_AND_SIGNIFICIANT_THROMBOCYTOPENIA)
                case _:  # case_0 or other
                    BAD_DATA_ERROR_MESSAGE: dict = Error.message("map_error")
        return json_dumps_ru(BAD_DATA_ERROR_MESSAGE)  # type: ignore


class CovidMapper(CaseMapper):

    """Class for mapping relevant interpretation for "covid" tests."""

    def __init__(self):
        """Initialize `CovidMapper` with boolean lists of entered data."""
        self.case_0 = []  # Error case
        self.case_1 = []  # UnfractionatedHeparin case
        self.case_2 = []  # LowMoleuclarWeightHeparin case

    def match_case(self) -> str:
        """Return an interpretation of the result by the correct combination
        of values or an error if no case matches.

        """
        for _case in vars(self).items():
            match _case:
                case "case_1", []:
                    pass
                case "case_2", []:
                    pass
                case _:  # case_0 or other
                    bad_data_error_message: dict = Error.message("map_error")  # noqa: F841
        # return json_dumps_ru(bad_data_error_message)
        return json_dumps_ru(
            Error.message(
                "emplemented_error",
                (None, "Отсутствует доказательная база."),
            )
        )
