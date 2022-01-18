"""Abstract classes."""
import abc


class CaseMapper(abc.ABC):

    """Abstract base class for mappers."""

    @abc.abstractclassmethod
    def match_case(self):
        """Abstract method to get an interpretation of the result
        by the correct combination of values.

        """
        raise NotImplementedError()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({vars(self)!r})"


class CaseSetter(abc.ABC):

    """Abstract base class for setters."""

    @abc.abstractclassmethod
    def _set(self):
        """Abstract method to set values to corresponding value cases."""
        raise NotImplementedError()

    @abc.abstractclassmethod
    def filter(self):
        """Abstract method to filter fields in which data entered."""
        raise NotImplementedError()

    @property
    @abc.abstractclassmethod
    def interpret_result(self):
        """Abstract method to set values to corresponding value cases
        and return rusult.

        """
        raise NotImplementedError()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.row_data!r})"

    def __str__(self) -> str:
        """Return interpretation of results."""
        return self._result


class BaseError(abc.ABC):

    """Abstract class for errors showing."""

    @staticmethod
    @abc.abstractclassmethod
    def message(error: str, data: tuple[str | None, str | None] = None) -> dict[str, str]:
        """Static abstract method to return error message by key (`error`).
        Optional parameter `data` is a tuple(title, description).

        """
        raise NotImplementedError()
