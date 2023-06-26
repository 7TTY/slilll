from flask import Flask
import json
import os


app = Flask(__name__)

from flask_app import routes
