from flask import render_template, request, redirect, url_for, flash

from flask_app import app

import sys


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/foo")
def foo():
    return "FOO"

@app.route("/bar")
def bar():
    return "BAR"
