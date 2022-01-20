"""Test "interpretation-of-thi-result" functionality."""
import re

import pytest
from werkzeug.datastructures import ImmutableMultiDict

from app import app
from app.interpretation.setters import ResultFetcher

app.testing = True
client = app.test_client()


URN = "/interpretation-of-results"
REGEX_PATTERN_ERROR = '<div class="flash error">'
REGEX_PATTERN_SUCCESS = '<div class="flash success">'
STATUS_CODE_OK = 200


@pytest.mark.parametrize(
    "request_form, expected",
    [
        # Test "case 0" (bad_data_error).
        (
            ImmutableMultiDict([("data_extem_ct", "1")]),
            '{"error": "bad_data_error", "title": "AAAAAAAAAAAAAAAAAA", \
"description": "Вы ввели недостаточно данных!"}',
        ),
        # Test "case 1" (HEMOSTASIS_CORRECTION_IS_NOT_SHOWN).
        (
            ImmutableMultiDict(
                [
                    ("data_extem_ct", "40"),
                    ("data_extem_a5", "37"),
                    ("data_intem_ct", "100"),
                    ("data_fibtem_a5", "8"),
                ]
            ),
            '{"title": "Коррекция гемостаза не показана", \
"description": "При коровотечении акцент на хирургический гемостаз"}',
        ),
        # Test "case 2" (DEFICIENCY_OF_FACTORS_EXTERNALLY).
        (
            ImmutableMultiDict(
                [
                    ("data_extem_ct", "80"),
                    ("data_fibtem_a5", "8"),
                ]
            ),
            '{"title": "Дефицит факторов внешнего пути", \
"description": "(Ауто)плазма 10-15 мл/кг или\\n\
Концентрат протромбинового комплекса (Протромплекс, Октаплекс)\\n\
CT EXTEM 81-100 сек - 7,5 МЕ/кг\\n\
CT EXTEM 101-120 сек - 15 МЕ/кг\\n\
CT EXTEM >120 сек – 22,5 МЕ/кг"}',
        ),
        # Test "case 3 subcase 1(range(240)" (HEPARIN_EFFECT).
        (
            ImmutableMultiDict(
                [
                    ("data_intem_ct", "240"),
                    ("data_heptem_ct", "239"),
                ]
            ),
            '{"title": "Эффект гепарина", \
"description": "Протамин 0,25-0,5 мг/кг"}',
        ),
        # Test "case 3 subcase 2(value < .8)" (HEPARIN_EFFECT).
        (
            ImmutableMultiDict(
                [
                    ("data_intem_ct", "0.6"),
                    ("data_heptem_ct", "0.7"),
                ]
            ),
            '{"title": "Эффект гепарина", \
"description": "Протамин 0,25-0,5 мг/кг"}',
        ),
        # Test "case 4" (DEFICIENCY_OF_FACTORS_INTERNALLY).
        (
            ImmutableMultiDict(
                [
                    ("data_intem_ct", "240"),
                    ("data_heptem_ct", "240"),
                ]
            ),
            '{"title": "Дефицит факторов внутреннего пути", \
"description": "(Ауто)плазма 10-15 мл/кг"}',
        ),
        # Test "case 5" (FIBRINOGEN_DEFICIENCY).
        (
            ImmutableMultiDict(
                [
                    ("data_extem_a5", "34"),
                    ("data_fibtem_a5", "7"),
                ]
            ),
            '{"title": "Дефицит фибриногена", \
"description": "Криопреципитат до достижения FIBTEM A5 10 мм (см. расчет дозы)"}',
        ),
        # FIXME: writeme: Test "case 6" (HIPERFIBRINOLYSIS).
        # Test "case 7" (SIGNIFICIANT_THROMBOCYTOPENIA).
        (
            ImmutableMultiDict(
                [
                    ("data_extem_a5", "34"),
                    ("data_fibtem_a5", "8"),
                ]
            ),
            '{"title": "Значимая тромбоцитопения", \
"description": "Тромбоцитный концентрат"}',
        ),
        # Test "case 8" (FIBRINOGEN_DEFICIENCY_AND_SIGNIFICIANT_THROMBOCYTOPENIA).
        (
            ImmutableMultiDict(
                [
                    ("data_extem_a5", "24"),
                    ("data_fibtem_a5", "7"),
                ]
            ),
            '{"title": "Дефицит фибриногена и значимая тромбоцитопения", \
"description": "Криопреципитат до достижения FIBTEM A5 10 мм (см. расчет дозы)\\n\
Тромбоцитный концентрат"}',
        ),
    ],
)
def test__ResulFetcher_with_surgery_category(request_form, expected):
    """Show 'interpretation-of-the-result' or error."""
    # Set into session clicked-category-test (ajax data)
    with client.session_transaction() as session:
        session["clicked_category_button"] = "surgery_category"
    # Tuplize  clicked-category-test and POST data
    post_data_with_session = session["clicked_category_button"], request_form
    # Get interpretation of the result
    request_interpreter = ResultFetcher(post_data_with_session)
    assert str(request_interpreter) == expected


@pytest.mark.parametrize(
    "POST_data, expected",
    [
        # Test "case 0" (bad_data_error).
        (
            {
                "data_extem_ct": "1",
            },
            REGEX_PATTERN_ERROR,
        ),
        # Test "case 1" (HEMOSTASIS_CORRECTION_IS_NOT_SHOWN).
        (
            {
                "data_extem_ct": "40",
                "data_extem_a5": "37",
                "data_intem_ct": "100",
                "data_fibtem_a5": "8",
            },
            REGEX_PATTERN_SUCCESS,
        ),
        # Test "case 2" (DEFICIENCY_OF_FACTORS_EXTERNALLY_.
        (
            {
                "data_extem_ct": "80",
                "data_fibtem_a5": "8",
            },
            REGEX_PATTERN_SUCCESS,
        ),
        # Test "case 3 subcase 1(range(240)" (HEPARIN_EFFECT).
        (
            {
                "data_intem_ct": "240",
                "data_heptem_ct": "239",
            },
            REGEX_PATTERN_SUCCESS,
        ),
        # Test "case 3 subcase 2(value < .8)" (HEPARIN_EFFECT).
        (
            {
                "data_intem_ct": "0.6",
                "data_heptem_ct": "0.7",
            },
            REGEX_PATTERN_SUCCESS,
        ),
        # Test "case 4" (DEFICIENCY_OF_FACTORS_INTERNALLY).
        (
            {
                "data_intem_ct": "240",
                "data_heptem_ct": "240",
            },
            REGEX_PATTERN_SUCCESS,
        ),
        # Test "case 5" (FIBRINOGEN_DEFICIENCY).
        (
            {
                "data_extem_a5": "34",
                "data_fibtem_a5": "7",
            },
            REGEX_PATTERN_SUCCESS,
        ),
        # FIXME: writeme: Test "case 6" (HIPERFIBRINOLYSIS).
        # Test "case 7" (SIGNIFICIANT_THROMBOCYTOPENIA).
        (
            {
                "data_extem_a5": "34",
                "data_fibtem_a5": "8",
            },
            REGEX_PATTERN_SUCCESS,
        ),
        # Test "case 8" (FIBRINOGEN_DEFICIENCY_AND_SIGNIFICIANT_THROMBOCYTOPENIA).
        (
            {
                "data_extem_a5": "24",
                "data_fibtem_a5": "7",
            },
            REGEX_PATTERN_SUCCESS,
        ),
    ],
)
def test__flash_message_has_expected_css_class(POST_data, expected):
    """Show success if user entered valid data or error."""
    # Set into session clicked-category-test (ajax data)
    with client.session_transaction() as session:
        session["clicked_category_button"] = "surgery_category"
    # POST data
    res = client.post(URN, data=POST_data)
    assert res.status_code == STATUS_CODE_OK
    # HTML document has flash message with .success or .error class
    regex_pattern = expected
    css_class = re.search(regex_pattern, str(res.data)).group()
    assert css_class == expected
