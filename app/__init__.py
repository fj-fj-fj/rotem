from flask import Flask

from app.settings.base import FlaskConfiguration


app = Flask(__name__)
app.config.from_object(FlaskConfiguration)


from app.views import routes  # noqa: F401 E402
