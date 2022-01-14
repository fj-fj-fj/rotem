from flask import abort
from flask import render_template
from flask import request

from app import app


@app.errorhandler(400)
def bad_request(error):
    return render_template("errors/400.html"), 400


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def internal_server(error):
    return render_template("errors/500.html", url=request.url), 500


@app.route("/__500")
def __500():
    abort(500)
