from flask import Flask


app = Flask(__name__)


from app.views import routes  # noqa: F401 E402
