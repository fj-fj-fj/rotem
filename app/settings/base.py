"""App configuration."""
import os
import sys


class BaseConfiguration:

    """Base configuration of the app."""

    @staticmethod
    def validate_python_version(file_with_version: str = ".python-minimal-version") -> None:
        """None if `sys.version_info` >= minimal Python version for this project or raise SystemExit."""

        def _make_versions_str_tuple(read_file: str) -> tuple[str, tuple[int, ...]]:
            """Return Python version as str and as tuple."""
            version_str: str = read_file.strip()
            version_tuple: tuple[int, ...] = tuple(int(n) for n in version_str.split(".") if n != ".")
            return version_str, version_tuple

        with open(file_with_version) as file:
            MININAL_VERSION_STR, MININAL_VERSION_TUPLE = _make_versions_str_tuple(file.read())

        # Display error if `sys.version_info` >= minimal Python version
        if sys.version_info < MININAL_VERSION_TUPLE:
            sys.exit("\033[31m" + f"This project requires Python version {MININAL_VERSION_STR} or newer" + "\033[39m")


class FlaskConfiguration(BaseConfiguration):

    """Set Flask configuration variables from .envrc file."""

    FLASK_APP: str | None = os.getenv("FLASK_APP")
    FLASK_ENV: str | None = os.getenv("FLASK_ENV")
    SECRET_KEY: str | None = os.getenv("FLASK_SECRET_KEY")
