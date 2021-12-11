import os


class FlaskConfiguration:

    FLASK_APP = os.getenv('FLASK_APP')
    FLASK_ENV = os.getenv('FLASK_ENV')
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
