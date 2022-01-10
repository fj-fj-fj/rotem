"""Test "interpretation-of-result" functionality."""
import json
import re

import pytest
from werkzeug.datastructures import ImmutableMultiDict

from app import app
from app.results_mapper import ResultInterpreter, show_results

app.testing = True
client = app.test_client()


URN = "/interpretation-of-results"
REGEX_PATTERN_ERROR = '<div class="flash error">'
REGEX_PATTERN_SUCCESS = '<div class="flash success">'
STATUS_CODE_OK = 200


@pytest.mark.parametrize(
    'request_form, expected',
    [
        # Test "case 0" or bad_data_error.
        # --------------------------------
        # Введены недостаточные или неверные данные.
        (
            ImmutableMultiDict([
                ('data_extem_ct', '1')
            ]),
            {
            'row_data':  # request.form
                {
                    'data_extem_ct': '1'
                },
            'case_mapper':  # results_mapper.CaseMapper instance
                {
                    'case_0': [True],
                    'case_1': [],
                    'case_2': [],
                    'case_3': [],
                    'case_4': [],
                    'case_5': [],
                    'case_6': [],
                    'case_7': [],
                    'case_8': []
                },
            'result':  # results_mapper.ResultInterpreter.result
                '{"error": "bad_data_error", "title": "Что-то тут не так!", \
"description": "Проверьте еще раз свои данные"}'
            }
        ),
        # Test "case 1" or HEMOSTASIS_CORRECTION_IS_NOT_SHOWN.
        # ----------------------------------------------------
        # Коррекция гемостаза не показана.
        (
            ImmutableMultiDict([
                ('data_extem_ct', '40'),  # in range(40, 81)
                ('data_extem_a5', '37'),  # in range(100, 240)
                ('data_intem_ct', '100'),  # in range(37, ResultInterpreter.MAXSIZE)
                ('data_fibtem_ct', ''),
                ('data_fibtem_a5', '8'),  # in range(8, ResultInterpreter.MAXSIZE)
                ('data_heptem_ct', ''),
                ('data_heptem_a5', ''),
                ('data_aptem_ct', ''),
                ('data_aptem_a5', ''),
                ('data_natem_ct', ''),
                ('data_natem_a5', '')
        ]),
        {
            'row_data':  # request.form
                {
                    'data_extem_ct': '40',
                    'data_extem_a5': '37',
                    'data_intem_ct': '100',
                    'data_fibtem_ct': '',
                    'data_fibtem_a5': '8',
                    'data_heptem_ct': '',
                    'data_heptem_a5': '',
                    'data_aptem_ct': '',
                    'data_aptem_a5': '',
                    'data_natem_ct': '',
                    'data_natem_a5': ''
                },
            'case_mapper':  # results_mapper.CaseMapper instance
                {
                    'case_0': [],
                    'case_1': [True, True, True, True],
                    'case_2': [True],
                    'case_3': [True],
                    'case_4': [],
                    'case_5': [],
                    'case_6': [],
                    'case_7': [True],
                    'case_8': []
                },
            'result':  # results_mapper.ResultInterpreter.result
                '{"title": "Коррекция гемостаза не показана", \
"description": "При коровотечении акцент на хирургический гемостаз"}'
            }
        ),
        # Test "case 2" or DEFICIENCY_OF_FACTORS_EXTERNALLY.
        # --------------------------------------------------
        # Дефицит факторов внешнего пути.
        (
            ImmutableMultiDict([
                ('data_extem_ct', '80'),  # in range(80, ResultInterpreter.MAXSIZE)
                ('data_extem_a5', ''),
                ('data_intem_ct', ''),
                ('data_fibtem_ct', ''),
                ('data_fibtem_a5', '8'),  # in range(8, ResultInterpreter.MAXSIZE)
                ('data_heptem_ct', ''),
                ('data_heptem_a5', ''),
                ('data_aptem_ct', ''),
                ('data_aptem_a5', ''),
                ('data_natem_ct', ''),
                ('data_natem_a5', '')
            ]),
            {
                'row_data':  # request.form
                    {
                        'data_extem_ct': '80',
                        'data_extem_a5': '',
                        'data_intem_ct': '',
                        'data_fibtem_ct': '',
                        'data_fibtem_a5': '8',
                        'data_heptem_ct': '',
                        'data_heptem_a5': '',
                        'data_aptem_ct': '',
                        'data_aptem_a5': '',
                        'data_natem_ct': '',
                        'data_natem_a5': ''
                    },
                'case_mapper':  # results_mapper.CaseMapper instance
                    {
                        'case_0': [],
                        'case_1': [True],
                        'case_2': [True, True],
                        'case_3': [],
                        'case_4': [],
                        'case_5': [],
                        'case_6': [],
                        'case_7': [True],
                        'case_8': []
                    },
            'result':  # results_mapper.ResultInterpreter.result
                '{"title": "Дефицит факторов внешнего пути", \
"description": "(Ауто)плазма 10-15 мл/кг или\\n\
Концентрат протромбинового комплекса (Протромплекс, Октаплекс)\\n\
CT EXTEM 81-100 сек - 7,5 МЕ/кг\\n\
CT EXTEM 101-120 сек - 15 МЕ/кг\\n\
CT EXTEM >120 сек – 22,5 МЕ/кг"}'
            }
        ),
        # Test "case 3 subcase 1(range(240)" or HEPARIN_EFFECT.
        # -----------------------------------------------------
        # Эффект гепарина.
        (
            ImmutableMultiDict([
                ('data_extem_ct', ''),
                ('data_extem_a5', ''),
                ('data_intem_ct', '240'),  # in range(240, ResultInterpreter.MAXSIZE) or if float(value) < .8
                ('data_fibtem_ct', ''),
                ('data_fibtem_a5', ''),
                ('data_heptem_ct', '239'),  # in range(240) or if float(value) < .8
                ('data_heptem_a5', ''),
                ('data_aptem_ct', ''),
                ('data_aptem_a5', ''),
                ('data_natem_ct', ''),
                ('data_natem_a5', '')
        ]),
        {
            'row_data':  # request.form
                {
                    'data_extem_ct': '',
                    'data_extem_a5': '',
                    'data_intem_ct': '240',
                    'data_fibtem_ct': '',
                    'data_fibtem_a5': '',
                    'data_heptem_ct': '239',
                    'data_heptem_a5': '',
                    'data_aptem_ct': '',
                    'data_aptem_a5': '',
                    'data_natem_ct': '',
                    'data_natem_a5': ''
                },
            'case_mapper':  # results_mapper.CaseMapper instance
                {
                    'case_0': [],
                    'case_1': [],
                    'case_2': [],
                    'case_3': [True, True],
                    'case_4': [True],
                    'case_5': [],
                    'case_6': [],
                    'case_7': [],
                    'case_8': []
                },
            'result':  # results_mapper.ResultInterpreter.result
                '{"title": "Эффект гепарина", \
"description": "Протамин 0,25-0,5 мг/кг"}'
            }
        ),
        # Test "case 3 subcase 2(value < .8)" or HEPARIN_EFFECT.
        # ------------------------------------------------------
        # Эффект гепарина.
        (
            ImmutableMultiDict([
                ('data_extem_ct', ''),
                ('data_extem_a5', ''),
                ('data_intem_ct', '.6'),  # in range(240, ResultInterpreter.MAXSIZE) or if float(value) < .8
                ('data_fibtem_ct', ''),
                ('data_fibtem_a5', ''),
                ('data_heptem_ct', '.7'),  # in range(240) or if float(value) < .8
                ('data_heptem_a5', ''),
                ('data_aptem_ct', ''),
                ('data_aptem_a5', ''),
                ('data_natem_ct', ''),
                ('data_natem_a5', '')
        ]),
        {
            'row_data':  # request.form
                {
                    'data_extem_ct': '',
                    'data_extem_a5': '',
                    'data_intem_ct': '.6',
                    'data_fibtem_ct': '',
                    'data_fibtem_a5': '',
                    'data_heptem_ct': '.7',
                    'data_heptem_a5': '',
                    'data_aptem_ct': '',
                    'data_aptem_a5': '',
                    'data_natem_ct': '',
                    'data_natem_a5': ''
                },
            'case_mapper':  # results_mapper.CaseMapper instance
                {
                    'case_0': [],
                    'case_1': [],
                    'case_2': [],
                    'case_3': [True, True],
                    'case_4': [],
                    'case_5': [],
                    'case_6': [],
                    'case_7': [],
                    'case_8': []
                },
            'result':  # results_mapper.ResultInterpreter.result
                '{"title": "Эффект гепарина", \
"description": "Протамин 0,25-0,5 мг/кг"}'
            }
        ),
        # Test "case 4" or DEFICIENCY_OF_FACTORS_INTERNALLY.
        # --------------------------------------------------
        # Дефицит факторов внутреннего пути.
        (
            ImmutableMultiDict([
                ('data_extem_ct', ''),
                ('data_extem_a5', ''),
                ('data_intem_ct', '240'),  # in range(240, ResultInterpreter.MAXSIZE)
                ('data_fibtem_ct', ''),
                ('data_fibtem_a5', ''),
                ('data_heptem_ct', '240'),   # in range(240, ResultInterpreter.MAXSIZE)
                ('data_heptem_a5', ''),
                ('data_aptem_ct', ''),
                ('data_aptem_a5', ''),
                ('data_natem_ct', ''),
                ('data_natem_a5', '')
            ]),
            {
                'row_data':  # request.form
                    {
                        'data_extem_ct': '',
                        'data_extem_a5': '',
                        'data_intem_ct': '240',
                        'data_fibtem_ct': '',
                        'data_fibtem_a5': '',
                        'data_heptem_ct': '240',
                        'data_heptem_a5': '',
                        'data_aptem_ct': '',
                        'data_aptem_a5': '',
                        'data_natem_ct': '',
                        'data_natem_a5': ''
                    },
                'case_mapper':  # results_mapper.CaseMapper instance
                    {
                        'case_0': [],
                        'case_1': [],
                        'case_2': [],
                        'case_3': [True],
                        'case_4': [True, True],
                        'case_5': [],
                        'case_6': [],
                        'case_7': [],
                        'case_8': []
                    },
            'result':  # results_mapper.ResultInterpreter.result
                '{"title": "Дефицит факторов внутреннего пути", \
"description": "(Ауто)плазма 10-15 мл/кг"}'
            }
        ),
        # Test "case 5" or FIBRINOGEN_DEFICIENCY.
        # ---------------------------------------
        # Дефицит фибриногена.
        (
            ImmutableMultiDict([
                ('data_extem_ct', ''),
                ('data_extem_a5', '34'),  # in range(25, 35)
                ('data_intem_ct', ''),
                ('data_fibtem_ct', ''),
                ('data_fibtem_a5', '7'),  # in range(8)
                ('data_heptem_ct', ''),
                ('data_heptem_a5', ''),
                ('data_aptem_ct', ''),
                ('data_aptem_a5', ''),
                ('data_natem_ct', ''),
                ('data_natem_a5', '')
            ]),
            {
                'row_data':  # request.form
                    {
                        'data_extem_ct': '',
                        'data_extem_a5': '34',
                        'data_intem_ct': '',
                        'data_fibtem_ct': '',
                        'data_fibtem_a5': '7',
                        'data_heptem_ct': '',
                        'data_heptem_a5': '',
                        'data_aptem_ct': '',
                        'data_aptem_a5': '',
                        'data_natem_ct': '',
                        'data_natem_a5': ''
                    },
                'case_mapper':  # results_mapper.CaseMapper instance
                    {
                        'case_0': [],
                        'case_1': [],
                        'case_2': [],
                        'case_3': [],
                        'case_4': [],
                        'case_5': [True, True],
                        'case_6': [],
                        'case_7': [True],
                        'case_8': [True]
                    },
            'result':  # results_mapper.ResultInterpreter.result
                '{"title": "Дефицит фибриногена", \
"description": "Криопреципитат до достижения FIBTEM A5 10 мм (см. расчет дозы)"}'
            }
        ),
        # FIXME: writeme: Test "case 6" or HIPERFIBRINOLYSIS.

        # Test "case 7" or SIGNIFICIANT_THROMBOCYTOPENIA.
        # -----------------------------------------------
        # Значимая тромбоцитопения.
        (
            ImmutableMultiDict([
                ('data_extem_ct', ''),
                ('data_extem_a5', '34'),  # in range(25, 35)
                ('data_intem_ct', ''),
                ('data_fibtem_ct', ''),
                ('data_fibtem_a5', '8'),  # in range(8, ResultInterpreter.MAXSIZE)
                ('data_heptem_ct', ''),
                ('data_heptem_a5', ''),
                ('data_aptem_ct', ''),
                ('data_aptem_a5', ''),
                ('data_natem_ct', ''),
                ('data_natem_a5', '')
            ]),
            {
                'row_data':  # request.form
                    {
                        'data_extem_ct': '',
                        'data_extem_a5': '34',
                        'data_intem_ct': '',
                        'data_fibtem_ct': '',
                        'data_fibtem_a5': '8',
                        'data_heptem_ct': '',
                        'data_heptem_a5': '',
                        'data_aptem_ct': '',
                        'data_aptem_a5': '',
                        'data_natem_ct': '',
                        'data_natem_a5': ''
                    },
                'case_mapper':  # results_mapper.CaseMapper instance
                    {
                        'case_0': [],
                        'case_1': [True],
                        'case_2': [True],
                        'case_3': [],
                        'case_4': [],
                        'case_5': [True],
                        'case_6': [],
                        'case_7': [True, True],
                        'case_8': []
                    },
            'result':  # results_mapper.ResultInterpreter.result
                '{"title": "Значимая тромбоцитопения", \
"description": "Тромбоцитный концентрат"}'
            }
        ),
        # Test "case 8" or FIBRINOGEN_DEFICIENCY_AND_SIGNIFICIANT_THROMBOCYTOPENIA.
        # -------------------------------------------------------------------------
        # Дефицит фибриногена и значимая тромбоцитопения.
        (
            ImmutableMultiDict([
                ('data_extem_ct', ''),
                ('data_extem_a5', '24'),  # in range(25)
                ('data_intem_ct', ''),
                ('data_fibtem_ct', ''),
                ('data_fibtem_a5', '7'),  # in range(8)
                ('data_heptem_ct', ''),
                ('data_heptem_a5', ''),
                ('data_aptem_ct', ''),
                ('data_aptem_a5', ''),
                ('data_natem_ct', ''),
                ('data_natem_a5', '')
            ]),
            {
                'row_data':  # request.form
                    {
                        'data_extem_ct': '',
                        'data_extem_a5': '24',
                        'data_intem_ct': '',
                        'data_fibtem_ct': '',
                        'data_fibtem_a5': '7',
                        'data_heptem_ct': '',
                        'data_heptem_a5': '',
                        'data_aptem_ct': '',
                        'data_aptem_a5': '',
                        'data_natem_ct': '',
                        'data_natem_a5': ''
                    },
                'case_mapper':  # results_mapper.CaseMapper instance
                    {
                        'case_0': [],
                        'case_1': [],
                        'case_2': [],
                        'case_3': [],
                        'case_4': [],
                        'case_5': [True],
                        'case_6': [],
                        'case_7': [True],
                        'case_8': [True, True]
                    },
            'result':  # results_mapper.ResultInterpreter.result
                '{"title": "Дефицит фибриногена и значимая тромбоцитопения", \
"description": "Криопреципитат до достижения FIBTEM A5 10 мм (см. расчет дозы)\\n\
Тромбоцитный концентрат"}'
            }
        ),

    ]
)
def test__show_results(request_form, expected):
    results_interpretation_row_data = json.loads(show_results(request_form))
    assert results_interpretation_row_data == expected


@pytest.mark.parametrize(
    'request_form, expected',
    [
        # Test "case 0" or bad_data_error.
        # --------------------------------
        # Введены недостаточные или неверные данные.
        (
            ImmutableMultiDict([
                ('data_extem_ct', 1)
            ]),
            '{"error": "bad_data_error", "title": "Что-то тут не так!", \
"description": "Проверьте еще раз свои данные"}',
        ),
        # Test "case 1" or HEMOSTASIS_CORRECTION_IS_NOT_SHOWN.
        # ----------------------------------------------------
        # Коррекция гемостаза не показана.
        (
            ImmutableMultiDict([
                ('data_extem_ct', 40),
                ('data_extem_a5', 37),
                ('data_intem_ct', 100),
                ('data_fibtem_a5', 8),
            ]),
            '{"title": "Коррекция гемостаза не показана", \
"description": "При коровотечении акцент на хирургический гемостаз"}'
        ),
        # Test "case 2" or DEFICIENCY_OF_FACTORS_EXTERNALLY.
        # --------------------------------------------------
        # Дефицит факторов внешнего пути.
        (
            ImmutableMultiDict([
                ('data_extem_ct', 80),
                ('data_fibtem_a5', 8),
            ]),
            '{"title": "Дефицит факторов внешнего пути", \
"description": "(Ауто)плазма 10-15 мл/кг или\\n\
Концентрат протромбинового комплекса (Протромплекс, Октаплекс)\\n\
CT EXTEM 81-100 сек - 7,5 МЕ/кг\\n\
CT EXTEM 101-120 сек - 15 МЕ/кг\\n\
CT EXTEM >120 сек – 22,5 МЕ/кг"}'
        ),
        # Test "case 3 subcase 1(range(240)" or HEPARIN_EFFECT.
        # -----------------------------------------------------
        # Эффект гепарина.
        (
            ImmutableMultiDict([
                ('data_intem_ct', 240),
                ('data_heptem_ct', 239),
            ]),
            '{"title": "Эффект гепарина", \
"description": "Протамин 0,25-0,5 мг/кг"}'
        ),
        # Test "case 3 subcase 2(value < .8)" or HEPARIN_EFFECT.
        # ------------------------------------------------------
        # Эффект гепарина.
        (
            ImmutableMultiDict([
                ('data_intem_ct', .6),
                ('data_heptem_ct', .7),
            ]),
            '{"title": "Эффект гепарина", \
"description": "Протамин 0,25-0,5 мг/кг"}'
        ),
        # Test "case 4" or DEFICIENCY_OF_FACTORS_INTERNALLY.
        # --------------------------------------------------
        # Дефицит факторов внутреннего пути.
        (
            ImmutableMultiDict([
                ('data_intem_ct', 240),
                ('data_heptem_ct', 240),
            ]),
            '{"title": "Дефицит факторов внутреннего пути", \
"description": "(Ауто)плазма 10-15 мл/кг"}'
        ),
        # Test "case 5" or FIBRINOGEN_DEFICIENCY.
        # ---------------------------------------
        # Дефицит фибриногена.
        (
            ImmutableMultiDict([
                ('data_extem_a5', 34),
                ('data_fibtem_a5', 7),
            ]),
            '{"title": "Дефицит фибриногена", \
"description": "Криопреципитат до достижения FIBTEM A5 10 мм (см. расчет дозы)"}'
        ),
        # FIXME: writeme: Test "case 6" or HIPERFIBRINOLYSIS.

        # Test "case 7" or SIGNIFICIANT_THROMBOCYTOPENIA.
        # -----------------------------------------------
        # Значимая тромбоцитопения.
        (
            ImmutableMultiDict([
                ('data_extem_a5', 34),
                ('data_fibtem_a5', 8),
            ]),
            '{"title": "Значимая тромбоцитопения", \
"description": "Тромбоцитный концентрат"}'
        ),
        # Test "case 8" or FIBRINOGEN_DEFICIENCY_AND_SIGNIFICIANT_THROMBOCYTOPENIA.
        # -------------------------------------------------------------------------
        # Дефицит фибриногена и значимая тромбоцитопения.
        (
            ImmutableMultiDict([
                ('data_extem_a5', 24),
                ('data_fibtem_a5', 7),
            ]),
            '{"title": "Дефицит фибриногена и значимая тромбоцитопения", \
"description": "Криопреципитат до достижения FIBTEM A5 10 мм (см. расчет дозы)\\n\
Тромбоцитный концентрат"}'
        ),
    ]
)
def test__ResulstInterpreter__str__(request_form, expected):
    request_interpreter = ResultInterpreter(request_form)
    assert str(request_interpreter) == expected


@pytest.mark.parametrize(
    'POST_data, expected',
    [
        # Test "case 0" or bad_data_error.
        # --------------------------------
        # Введены недостаточные или неверные данные.
        (
            {
                "data_extem_ct": 1,
            },
            REGEX_PATTERN_ERROR,
        ),
        # Test "case 1" or HEMOSTASIS_CORRECTION_IS_NOT_SHOWN.
        # ----------------------------------------------------
        # Коррекция гемостаза не показана.
        (
            {
                'data_extem_ct': 40,
                'data_extem_a5': 37,
                'data_intem_ct': 100,
                'data_fibtem_a5': 8,
            },
            REGEX_PATTERN_SUCCESS,
        ),
        # Test "case 2" or DEFICIENCY_OF_FACTORS_EXTERNALLY.
        # --------------------------------------------------
        # Дефицит факторов внешнего пути.
        (
            {
                'data_extem_ct': 80,
                'data_fibtem_a5': 8,
            },
            REGEX_PATTERN_SUCCESS,
        ),
        # Test "case 3 subcase 1(range(240)" or HEPARIN_EFFECT.
        # -----------------------------------------------------
        # Эффект гепарина.
        (
            {
                'data_intem_ct': 240,
                'data_heptem_ct': 239,
            },
            REGEX_PATTERN_SUCCESS,
        ),
        # Test "case 3 subcase 2(value < .8)" or HEPARIN_EFFECT.
        # ------------------------------------------------------
        # Эффект гепарина.
        (
            {
                'data_intem_ct': .6,
                'data_heptem_ct': .7,
            },
            REGEX_PATTERN_SUCCESS,
        ),
        # Test "case 4" or DEFICIENCY_OF_FACTORS_INTERNALLY.
        # --------------------------------------------------
        # Дефицит факторов внутреннего пути.
        (
            {
                'data_intem_ct': 240,
                'data_heptem_ct': 240,
            },
            REGEX_PATTERN_SUCCESS,
        ),
        # Test "case 5" or FIBRINOGEN_DEFICIENCY.
        # ---------------------------------------
        # Дефицит фибриногена.
        (
            {
                'data_extem_a5': 34,
                'data_fibtem_a5': 7,
            },
            REGEX_PATTERN_SUCCESS,
        ),
        # FIXME: writeme: Test "case 6" or HIPERFIBRINOLYSIS.

        # Test "case 7" or SIGNIFICIANT_THROMBOCYTOPENIA.
        # -----------------------------------------------
        # Значимая тромбоцитопения.
        (
            {
                'data_extem_a5': 34,
                'data_fibtem_a5': 8,
            },
            REGEX_PATTERN_SUCCESS,
        ),
        # Test "case 8" or FIBRINOGEN_DEFICIENCY_AND_SIGNIFICIANT_THROMBOCYTOPENIA.
        # -------------------------------------------------------------------------
        # Дефицит фибриногена и значимая тромбоцитопения.
        (
            {
                'data_extem_a5': 24,
                'data_fibtem_a5': 7,
            },
            REGEX_PATTERN_SUCCESS,
        ),
    ]
)
def test__flash_message_has_expected_css_class(POST_data, expected):
    res = client.post(URN, data=POST_data)
    assert res.status_code == STATUS_CODE_OK
    regex_pattern = expected
    css_class = re.search(regex_pattern, str(res.data)).group()
    assert css_class == expected
