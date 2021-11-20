from app import app
from flask import render_template


@app.route('/')
def index_view():
    return render_template('index.html')


@app.route('/about/')
def about_view():
    return render_template('about.html')


@app.route('/tests/')
def rotem_tests_view():
    return render_template('tests.html')


@app.route('/historical_data')
def historical_data_view():
    return render_template('historical_data.html')


@app.route('/parameters/')
def rotem_parameters_view():
    return render_template('parameters.html')


@app.route('/video-instructions/')
def video_instructions_view():
    return render_template('video_instructions.html')


@app.route('/interpretation-of-results/')
def results_interpretation_view():
    return render_template('results_interpretation.html')


@app.route('/help/')
def help_view():
    return render_template('help.html')


@app.route('/useful-links/')
def useful_links_view():
    return render_template('useful_links.html')
