#!/usr/bin/env python
from app import app
from app.settings.base import FlaskConfiguration


if __name__ == "__main__":
    FlaskConfiguration.validate_python_version()
    app.run()
