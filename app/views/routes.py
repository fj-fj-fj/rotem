from datetime import datetime

from flask import render_template

from app import app
from app.breadcrumbs import register_breadcrumb
from app.menu import menu
from app.news import fetch_all_articles
from app.views.errors import *  # noqa: F401 F403
from app.views.menu import *  # noqa: F401 F403


@app.context_processor
def common_data():
    return {
        'menu': menu,
        'current_year': datetime.now().year,
    }


@app.route('/news')
@app.route('/')
@register_breadcrumb('Новости')
def index():
    all_articles = fetch_all_articles()['articles']
    return render_template('index.html', articles=all_articles)
