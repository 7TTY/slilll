from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from passlib.hash import sha256_crypt

from flask_app import app, db
from flask_app.models import User, Post
from flask_app.forms import PostForm

import sys


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/spotify-test", methods=['GET','POST'])
def spotify_test():
    if request.method == 'GET':
        #print('getting spotify-test.html', file=sys.stderr)
        return render_template("spotify-test.html")
    else:
        if request.form.get('submit_button') == 'Foo':
            #print('Go To Google', file=sys.stderr)
            #pass # do something
            return redirect(url_for("foo"))

        elif request.form.get('submit_button') == 'Bar':
            #print('Go To Wikipedia', file=sys.stderr)
            #pass # do something else

            return redirect(url_for("bar"))
        else:
            pass # unknown

@app.route("/foo")
def foo():
    return "FOO"

@app.route("/bar")
def bar():
    return "BAR"
