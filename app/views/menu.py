from flask import flash
from flask import render_template
from flask import request

from app.breadcrumbs import register_breadcrumb


from app import app


@app.route('/about')
@register_breadcrumb('информация о rotem', aside_menu=True)
def about():
    return render_template('menu/about.html')


@app.route('/tests')
@register_breadcrumb('тесты rotem', aside_menu=True)
def tests():
    return render_template('menu/tests.html')


@app.route('/historical-data')
@register_breadcrumb('историческая справка', aside_menu=True)
def historical_data():
    return render_template('menu/historical_data.html')


@app.route('/video-instructions')
@register_breadcrumb('видео инструкции', aside_menu=True)
def video_instructions():
    return render_template('menu/video_instructions.html')


@app.route('/interpretation-of-results', methods=['GET', 'POST'])
@register_breadcrumb('интерпретация результатов', aside_menu=True)
def results_interpretation():
    if request.method == 'POST':
        if len(request.form['username']) >= 2:
            flash('Succsess! :)', category='success')
        else:
            flash('Error! :(', category='error')
    return render_template('menu/results_interpretation.html')


@app.route('/help')
@register_breadcrumb('поддержка', aside_menu=True)
def help():
    return render_template('menu/help.html')


@app.route('/useful-links')
@register_breadcrumb('полезные ссылки', aside_menu=True)
def useful_links():
    return render_template('menu/useful_links.html')
