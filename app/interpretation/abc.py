"""Abstract classes."""
import abc
from typing import Literal


class CaseMapper(abc.ABC):

    """Abstract base class for mappers."""

    @abc.abstractclassmethod
    def match_case(self) -> None:
        """Abstract method to get an interpretation of the result
        by the correct combination of values.

        Return interpretation of the result or an error if no case matches.
        """
        raise NotImplementedError()

    def __repr__(self) -> str:
        """Return class name with self.__dict__."""
        return f"{self.__class__.__name__}({vars(self)!r})"


class CaseSetter(abc.ABC):

    """Abstract base class for setters."""

    MAXSIZE: Literal[1000] = 1000
    """The maximum possible value for input data."""

    # Input data. See `CaseSetter.filter().__doc__`. __init__ attribute.
    row_data: dict = {}
    # ObstericMapper, SurgeryMapper or CovidMapper instance. __init__ attribute.
    case_mapper = "CaseMapper"  # type: ignore
    # Interpretation of the result. __init__ attribute.
    _result = ""

    @abc.abstractclassmethod
    def _set(self) -> None:
        """Abstract method to set values to corresponding value cases."""
        raise NotImplementedError()

    def __repr__(self) -> str:
        """Return class name with input data."""
        return f"{self.__class__.__name__}({self.row_data!r})"

    def __str__(self) -> str:
        """Return interpretation of the results."""
        return self._result

    def filter(self) -> list[tuple[str, str]]:
        """Return fltered fields where second value is int or float.

        Input data example:
            ImmutableMultiDict([
                ('data_extem_ct', '1')
                ('data_extem_a5', '0.8')
                ('data_intem_ct', 'span'),
                ('data_fibtem_a5', 'True'),
                ('data_heptem_ct', '')
            ])
        Filtered data:
            ImmutableMultiDict([
                ('data_extem_ct', '1')
                ('data_extem_a5', '0.8')
            ])

        """
        return [(name, value) for name, value in self.row_data.items() if value and not value.isalpha()]

    def handle(self) -> str:
        """Set values to corresponding value cases and return rusult."""
        # Set values to corresponding value cases
        self._set()
        # Return result
        result: dict = self.case_mapper.match_case()  # type: ignore
        return str(result)


class BaseError(abc.ABC):

    """Abstract class for errors showing."""

    @staticmethod
    @abc.abstractclassmethod
    def message(error: str, data: tuple[str | None, str | None] = None) -> dict[str, str]:
        """Static abstract method to return error message by key.

        Optional parameter `data` is a tuple(title, description) to pass in
        error message.

        Error message example:
            "blood_error": {
                "error": "not_emplemented_error",
                "title": `title` or "Функциональность пока не реализована",
                "description": `description` or "Должна пролиться кровь.",
            }
        Error message fetching:
            return dict(
                'error1': {msg1}, 'error2': {msg2}, 'error3': {msg3}, ...
            )[`error`]

        """
        raise NotImplementedError()
