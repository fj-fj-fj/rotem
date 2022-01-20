"""This module contains errors, exceptions, warnings.

Classes: `Error()`.

"""
from app.interpretation.abc import BaseError


# Error() exports to app.interetation.mappers, app.interetation.setters
__all__ = ("Error",)


class Error(BaseError):

    """Class for error messages showing."""

    @staticmethod
    def message(error: str, data: tuple[str | None, str | None] = None) -> dict[str, str]:
        """Static method to return error message by key (`error` parameter).
        Optional parameter `data` is a tuple(title, description).

        """
        title, description = data if data else (None, None)
        return {
            "session_error": {
                "error": "session_data_error",
                "title": title or "AAAAAAAAAAAAAAAAAA",
                "description": description or "wtf wtf wtf ?",
            },
            "map_error": {
                "error": "bad_data_error",
                "title": title or "AAAAAAAAAAAAAAAAAA",
                "description": description or "Вы ввели недостаточно данных!",
            },
            "emplemented_error": {
                "error": "not_emplemented_error",
                "title": title or "Функциональность пока не реализована",
                "description": description or "",
            },
        }.get(error, "meta_error")
