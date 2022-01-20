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

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.row_data!r})"

    def __str__(self) -> str:
        """Return interpretation of results."""
        return self._result

    def filter(self) -> list[tuple[str, str]]:
        """Return fltered fields where second value is int or float.

        Example data entered:
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
        self._set()
        result: dict = self.case_mapper.match_case()
        return str(result)


class BaseError(abc.ABC):

    """Abstract class for errors showing."""

    @staticmethod
    @abc.abstractclassmethod
    def message(error: str, data: tuple[str | None, str | None] = None) -> dict[str, str]:
        """Static abstract method to return error message by key.

        Optional parameter `data` is a tuple(title, description) to pass in
        error message.

        Message error example:
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

    def __repr__(self) -> str:
        return f"{type(self).__name__}(error={self.error!r}, data={(self.data[0], self.data[1])!r})"
