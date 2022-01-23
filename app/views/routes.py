"""Module contains Index endpoit and `context_processor` functions."""
from datetime import datetime

from flask import render_template

from app import app
from app.breadcrumbs import register_breadcrumb
from app.menu import menu_name_url_map
from app.news import fetch_all_articles
from app.views.errors import *  # noqa: F401 F403
from app.views.menu import *  # noqa: F401 F403


@app.context_processor
def common_data():
    return {
        "menu": menu_name_url_map,
        "current_year": datetime.now().year,
    }


@app.route("/news")
@app.route("/")
@register_breadcrumb("Новости")
def index():
    all_articles = fetch_all_articles()["articles"]
    return render_template("index.html", articles=all_articles)


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint.

    (see the HEALTHCHECK instruction in ./Dockerfile).

    """
    # Handle here any business logic for ensuring you're application
    # is healthy (DB connections, etc...)
    return "Healthy: OK"
