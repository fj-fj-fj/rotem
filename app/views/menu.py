"""Menu endpoints."""
import json

from flask import flash
from flask import render_template
from flask import request
from flask import session

from app.breadcrumbs import register_breadcrumb
from app.interpretation import show_results


from app import app


@app.route("/about")
@register_breadcrumb("информация о rotem", aside_menu=True)
def about():
    return render_template("menu/about.html")


@app.route("/tests")
@register_breadcrumb("тесты rotem", aside_menu=True)
def tests():
    return render_template("menu/tests.html")


@app.route("/historical-data")
@register_breadcrumb("историческая справка", aside_menu=True)
def historical_data():
    return render_template("menu/historical_data.html")


@app.route("/video-instructions")
@register_breadcrumb("видео инструкции", aside_menu=True)
def video_instructions():
    return render_template("menu/video_instructions.html")


@app.route("/interpretation-of-results", methods=["GET", "POST"])
@register_breadcrumb("интерпретация результатов", aside_menu=True)
def results_interpretation():
    if request.method == "POST":

        # ajax data: clicked category button.
        # one of: 'obsteric_category' | 'surgery_category' | 'covid_category'.
        if category := [c for c in request.form if "clicked_category_button" in c]:
            cat: dict = json.loads(category[0])
            session["clicked_category_button"] = cat["clicked_category_button"]
            return render_template("menu/results_interpretation.html")

        # flash message: interpretation of result or error.
        row_data = json.loads(show_results(request.form))
        interpretation_of_result_data = row_data.get("_result")
        if not interpretation_of_result_data:
            return render_template("menu/results_interpretation.html")
        result = json.loads(interpretation_of_result_data)
        if result.get("error"):
            flash(result, category="error")
        else:
            flash(result, category="success")

    return render_template("menu/results_interpretation.html")


@app.route("/help")
@register_breadcrumb("поддержка", aside_menu=True)
def help():
    return render_template("menu/help.html")


@app.route("/useful-links")
@register_breadcrumb("полезные ссылки", aside_menu=True)
def useful_links():
    return render_template("menu/useful_links.html")
