from flask import flash, render_template, request

from app import app


@app.route('/about')
def about():
    return render_template('menu/about.html')


@app.route('/tests')
def tests():
    return render_template('menu/tests.html')


@app.route('/historical-data')
def historical_data():
    return render_template('menu/historical_data.html')


@app.route('/parameters')
def parameters():
    return render_template('menu/parameters.html')


@app.route('/video-instructions/work')
def video_instructions_work():
    return render_template('menu/video_instructions_work.html')


@app.route('/video-instructions/smth')
def video_instructions_smth():
    return render_template('menu/video_instructions_smth.html')


@app.route('/interpretation-of-results', methods=['GET', 'POST'])
def results_interpretation():
    if request.method == 'POST':
        if len(request.form['username']) >= 2:
            flash('Succsess! :)', category='success')
        else:
            flash('Error! :(', category='error')
    return render_template('menu/results_interpretation.html')


@app.route('/help')
def help():
    return render_template('menu/help.html')


@app.route('/useful-links')
def useful_links():
    return render_template('menu/useful_links.html')
