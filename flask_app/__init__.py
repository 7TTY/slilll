from flask import Flask
import json
import os


app = Flask(__name__)

#app.config['SECRET_KEY'] = os.urandom(64)
#app.config['SESSION_TYPE'] = 'filesystem'
#app.config['SESSION_FILE_DIR'] = './.flask_session/'


#with open('/home/utterpop/slilll/flask_app/config.json') as config_file:
#	config = json.load(config_file)

#app.config['CLIENT_ID'] = config.get('CLIENT_ID')
#app.config['CLIENT_SECRET'] = config.get('CLIENT_SECRET')

from flask_app import routes
