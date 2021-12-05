from flask import render_template

from app import app
from app.menu import menu
from app.news import fetch_all_articles
from app.views.menu import *  # noqa: F401 E402


@app.context_processor
def show_menu():
    return {'menu': menu}


@app.route('/news')
@app.route('/')
def index():
    all_articles = fetch_all_articles()['articles']
    return render_template(
        'index.html',
        articles=all_articles,
    )
