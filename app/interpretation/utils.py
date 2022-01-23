import json
from typing import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.interpretation.setters import _Setter

    _SETTER_OR_DICT = _Setter | dict


def json_dumps_ru(interpretation_data: "_SETTER_OR_DICT", default: Callable = None) -> str:
    """`json.dumps with `ensure_ascii=False`.

    Return value can contain non-ASCII characters if they appear in strings
    contained in obj. Otherwise, all such characters are escaped in JSON strings.

    """
    return json.dumps(interpretation_data, ensure_ascii=False, default=default)
