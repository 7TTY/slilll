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

#change port
# redirect_uri = http://127.0.0.1:8080/callback

#  Client Keys
import yaml
import base64

with open('/home/utterpop/slilll/flask_app/config.yaml', 'r') as file:
	client_keys = yaml.safe_load(file)


CLIENT_ID = client_keys['client_keys']['client_id']
CLIENT_SECRET = client_keys['client_keys']['client_id']

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
#CLIENT_SIDE_URL = "http://127.0.0.1"
#change port
#PORT = 8000
#removed /q
#REDIRECT_URI = "{}:{}/spotify/callback".format(CLIENT_SIDE_URL, PORT)

# test out public ip /callback -- register as redirect uri 
REDIRECT_URI = "http://173.230.144.62/spotify/callback"


SCOPE = "playlist-modify-public playlist-modify-private"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()


@app.route("/spotify/authorize")
def spotify_authorize():
    # Auth Step 1: Authorization

    auth_query_parameters = {
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        # "state": STATE,
        # "show_dialog": SHOW_DIALOG_str,
        "client_id": CLIENT_ID
    }
    authorize_url = 'https://accounts.spotify.com/en/authorize?'
    parameters = 'response_type=code&client_id=' + CLIENT_ID + '&redirect_uri=' + REDIRECT_URI + '&scope=' + SCOPE
    response = make_response(redirect(authorize_url + parameters))

    return response
#    url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()])
#    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
#    return redirect(auth_url)

@app.route("/spotify/callback")
def spotify_callback():
    # Auth Step 4: Requests refresh and access tokens
    code = request.args['code']

    base64encoded = base64.b64encode(("{}:{}".format(CLIENT_ID, CLIENT_SECRET)).encode())
    headers = {
#        'Authorization': "Basic {}".format(base64encoded.decode()),
        'Authorization': "Basic {}".format(base64encoded)
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    body = {
        "code": str(code),
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }


    post_response = requests.post(SPOTIFY_TOKEN_URL, headers=headers, data=body)

    if post_response.status_code == 200:
        pr = post_response.json()
        return str([pr['access_token'], pr['refresh_token'], pr['expires_in']])
    else:
#        logging.error('getToken:' + str(post_response.status_code))
        error_message = "ERROR\n"
        error_message += str(headers) + str(body)
        return error_message
    # Auth Step 5: Tokens are Returned to Application
#    print(post_request)
#    response_data = json.loads(post_request.text)
#    access_token = response_data["access_token"]
#    refresh_token = response_data["refresh_token"]
#    token_type = response_data["token_type"]
#    expires_in = response_data["expires_in"]


    # Get profile data
#    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
#    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
#    profile_data = json.loads(profile_response.text)

    # Get user playlist data
#    playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
#    playlists_response = requests.get(playlist_api_endpoint, headers=authorization_header)
#    playlist_data = json.loads(playlists_response.text)

    # Combine profile and playlist data to display
#    display_arr = [profile_data] + playlist_data["items"]
#    return render_template("index.html", sorted_array=display_arr)


#example Medium article
#@app.route("/spotify/authorize")
#def spotify_authorize():
#	client_id = app.config['CLIENT_ID']
#	client_secret = app.config['CLIENT_SECRET']
#	redirect_uri = app.config['REDIRECT_URI']
#	scope = app.config['SCOPE']
#
#	# state key used to protect against cross-site forgery attacks
#	state_key = createStateKey(15)
#	session['state_key'] = state_key
#
#	# redirect user to Spotify authorization page
#	authorize_url = 'https://accounts.spotify.com/en/authorize?'
#	parameters = 'response_type=code&client_id=' + client_id + '&redirect_uri=' + redirect_uri + '&scope=' + scope + '&state=' + state_key
#	response = make_response(redirect(authorize_url + parameters))
#
#	return response


#@app.route("spotify/callback")
#def spotify_callback():
#	# make sure the response came from Spotify
#	if request.args.get('state') != session['state_key']:
#		return render_template('index.html', error='State failed.')
#	if request.args.get('error'):
#		return render_template('index.html', error='Spotify error.')
#	else:
#		code = request.args.get('code')
#		session.pop('state_key', None)
#
#		# get access token to make requests on behalf of the user
#		payload = getToken(code)
#		if payload != None:
#			session['token'] = payload[0]
#			session['refresh_token'] = payload[1]
#			session['token_expiration'] = time.time() + payload[2]
#		else:
#			return render_template('index.html', error='Failed to access token.')
#
#	current_user = getUserInformation(session)
#	session['user_id'] = current_user['id']
#	logging.info('new user:' + session['user_id'])
#
#	return redirect(session['previous_url'])


