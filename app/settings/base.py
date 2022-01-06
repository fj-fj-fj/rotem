import os
import sys


class BaseConfiguration:

    @staticmethod
    def validate_python_version(file_with_version: str = '.python-minimal-version'):
        """None if `sys.version_info` >= minimal Python version for this project or raise SystemExit."""
        def _make_versions_str_tuple(read_file):
            version_str: str = read_file.strip()
            version_tuple: tuple[int, ...] = tuple(int(n) for n in version_str.split('.') if n != '.')
            return version_str, version_tuple

        with open(file_with_version) as file:
            MININAL_VERSION_STR, MININAL_VERSION_TYPLE = _make_versions_str_tuple(file.read())

        if sys.version_info < MININAL_VERSION_TYPLE:
            sys.exit("\033[31m" + f"This project requires Python version {MININAL_VERSION_STR} or newer" + "\033[39m")


class FlaskConfiguration(BaseConfiguration):

    FLASK_APP = os.getenv('FLASK_APP')
    FLASK_ENV = os.getenv('FLASK_ENV')
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
