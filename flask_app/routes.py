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

# considering adding scope as variable to session dict? can i do that?


# @app.route( INDEX_URI )
def __session_prep():
    
    scope = session.get('spotify_scope', None)

    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        scope=scope,
        client_id= CLIENT_ID,
        client_secret= CLIENT_SECRET,
        redirect_uri= REDIRECT_URI,
        cache_handler=cache_handler,
        show_dialog=True
    )
    return cache_handler, auth_manager

# show dialog True when loggin in, otherwise False ??


@app.route( INDEX_URI )
def spotify_redirect_uri():
    
    #scope = 'user-read-currently-playing'
    #scope = None
    #cache_handler, auth_manager = __session_prep(scope=scope)
    # session['spotify_scope'] = 
    cache_handler, auth_manager = __session_prep()
    if request.args.get("code"):
        # Step 2. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect( INDEX_URI )    
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 1. Display sign in link when no token
        return redirect( INDEX_URI + '/sign-in' )

    return f'<a href="{ INDEX_URI }/playlists">my playlists</a> | ' \
            f'<a href="{ INDEX_URI }/current-user">me</a> | ' \
            f'<a href="{ INDEX_URI }/sign-out">sign-out</a>'



@app.route( INDEX_URI + '/sign-in' )
def spotify_sign_in():
    
    #scope = 'user-read-currently-playing'
    #scope = None
    cache_handler, auth_manager = __session_prep()
    if auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect( INDEX_URI )
    else:
        auth_url = auth_manager.get_authorize_url()
        return f'<h2><a href="{auth_url}">Sign in</a></h2>'       



@app.route( INDEX_URI + '/sign-out')
def spotify_sign_out():
    session.pop("token_info", None)
    session.pop('scope', None) 
    return redirect( INDEX_URI )



@app.route( INDEX_URI + '/playlists')
def playlists():
    
    #scope = 'user-read-currently-playing'
    session['spotify_scope'] = 'user-read-currently-playing'
    cache_handler, auth_manager = __session_prep()
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect( INDEX_URI + '/sign-in' )

    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify.current_user_playlists()

@app.route( INDEX_URI + '/current-user')
def current_user():
    
    #scope = 'user-read-currently-playing'
    session['spotify_scope'] = 'user-read-currently-playing'
    cache_handler, auth_manager = __session_prep()
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect( INDEX_URI + '/sign-in' )
    
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify.current_user()

