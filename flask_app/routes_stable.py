#from flask import render_template, request, redirect, url_for, flash

from flask_app import app
from flask import url_for

from flask import render_template, flash, redirect, request, session, make_response, jsonify, abort

#spotify example https://github.com/drshrey/spotify-flask-auth-example/blob/master/main.py
import json
from flask import Flask, request, redirect, g, render_template
import requests
from urllib.parse import quote

#spotify example Medium article
#from main import app
#from functions import createStateKey, getToken, refreshToken, checkTokenStatus, getUserInformation, getAllTopTracks, getTopTracksID, getTopTracksURI, getTopArtists, getRecommendedTracks, startPlayback, startPlaybackContext, pausePlayback, shuffle, getUserPlaylists, getUserDevices, skipTrack, getTrack, getTrackAfterResume, createPlaylist, addTracksPlaylist, searchSpotify
#from models import addUser
#import time
#import logging


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/foo")
def foo():
#    return "FOO"
	return redirect("https://www.google.com")

@app.route("/bar")
def bar():
    return redirect("https://rationalwiki.org/wiki/Main_Page")

#
#
#spotify
#
#

"""
Prerequisites

    pip3 install spotipy Flask Flask-Session

    // from your [app settings](https://developer.spotify.com/dashboard/applications)
    export SPOTIPY_CLIENT_ID=client_id_here
    export SPOTIPY_CLIENT_SECRET=client_secret_here
    export SPOTIPY_REDIRECT_URI='http://127.0.0.1:8080' // must contain a port
    // SPOTIPY_REDIRECT_URI must be added to your [app settings](https://developer.spotify.com/dashboard/applications)
    OPTIONAL
    // in development environment for debug output
    export FLASK_ENV=development
    // so that you can invoke the app outside of the file's directory include
    export FLASK_APP=/path/to/spotipy/examples/app.py

    // on Windows, use `SET` instead of `export`

Run app.py

    python3 app.py OR python3 -m flask run
    NOTE: If receiving "port already in use" error, try other ports: 5000, 8090, 8888, etc...
        (will need to be updated in your Spotify app and SPOTIPY_REDIRECT_URI variable)
"""

# deployment redirect uri --> http://173.230.144.62/spotify

from flask import Flask, session, request, redirect
from flask_session import Session
import spotipy
import os

# already defined app before
#app = Flask(__name__)

with open('/home/utterpop/slilll/flask_app/config.json') as config_file:
   config = json.load(config_file)

CLIENT_ID = config.get('CLIENT_ID')
CLIENT_SECRET = config.get('CLIENT_SECRET')
REDIRECT_URI = config.get('REDIRECT_URI')

app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'

# start session for Flask Session Cache Handler:
# cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
Session(app)

INDEX_URI = '/spotify'

@app.route( INDEX_URI + '/sign-in' )
def spotify_auth():

    scope='user-read-currently-playing'
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        scope=scope,
        client_id= CLIENT_ID,
        client_secret= CLIENT_SECRET,
        redirect_uri= REDIRECT_URI,
        cache_handler=cache_handler,
        show_dialog=True
    )
    
    if request.args.get("code"):
        # Step 2. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect( INDEX_URI )

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 1. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return f'<h2><a href="{auth_url}">Sign in</a></h2>'

    # Step 3. Signed in, display data
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return f'<h2>Hi {spotify.me()["display_name"]}, ' \
           f'<small><a href="/spotify/sign_out">[sign out]<a/></small></h2>' \
           f'<a href="/spotify/playlists">my playlists</a> | ' \
        	f'<a href="/spotify/current_user">me</a>' \



@app.route( INDEX_URI + '/sign_out')
def sign_out():
    session.pop("token_info", None)
    return redirect( INDEX_URI )



@app.route( INDEX_URI + '/playlists')
def playlists():
    
#    scope = 'playlist-modify-private'
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(
#        scope=scope,
        client_id= CLIENT_ID,
        client_secret= CLIENT_SECRET,
        redirect_uri= REDIRECT_URI,
        cache_handler=cache_handler,
#        show_dialog=True
    )

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect( INDEX_URI )

    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify.current_user_playlists()


@app.route( INDEX_URI + '/current_user')
def current_user():
    
#    scope = 'playlist-modify-private'
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(
#        scope=scope,
        client_id= CLIENT_ID,
        client_secret= CLIENT_SECRET,
        redirect_uri= REDIRECT_URI,
        cache_handler=cache_handler,
#        show_dialog=True
    )

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect( INDEX_URI )
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify.current_user()

#def use_access_token():
#
#    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
#    auth_manager = spotipy.oauth2.SpotifyOAuth(
#        client_id= CLIENT_ID,
#        client_secret= CLIENT_SECRET,
#        redirect_uri= REDIRECT_URI,
#        cache_handler=cache_handler
#    )

#    return cache_handler, auth_manager