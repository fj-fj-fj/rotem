from contextlib import contextmanager
from typing import Generator

from flask import Flask
from flask import template_rendered
from jinja2.environment import Template


@contextmanager
def captured_templates(app: Flask) -> Generator[list, None, None]:
    """
    A helper context manager that can be used in a unittest
    to determine which templates were rendered and what variables
    were passed to the template.
    """
    recorded = []

    def record(sender: Flask, template: Template, context: dict, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)
