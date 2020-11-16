#!/usr/bin/env python

#=====================|
#     APP IMPORTS     |
#                     |
#=====================|
import datetime
import os
from flask_pymongo import PyMongo
import pymongo
from flask import url_for, session, Flask, redirect, render_template, request, flash
from werkzeug.utils import secure_filename
import config
from flask_discord import DiscordOAuth2Session
import asyncio
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import requests
from bs4 import BeautifulSoup
import random
import string
import asyncio
from flask import Response

#=====================|
#     APP CONFIG      |
#                     |
#=====================|

DEBUG = True
app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["20 per minute"]
)

embeds = {}

regular = '<head>\n<meta name="title" content="Hiven Embed Generator">\n<meta name="description" content="make a post request to this URL with the parameters description and title to set this embed">\n</head>'
template = '<head>\n<meta name="title" content=":TITLE:">\n<meta name="description" content=":DESC:">\n</head>'

#=====================|
#     APP ROUTES      |
#                     |
#=====================|

# index route
@app.route("/<name>", methods=['GET', 'POST'])
def index(name):
    if name is None:
        return regular
    else:
        if request.method == 'POST':
            embeds[name] = {'title': request.args['title'], 'description': request.args['description']}
        elif request.method == 'GET':
            if name in embeds.keys():
                return template.replace(":TITLE:", embeds[name]['title']).replace(":DESC:", embeds[name]['description'])
            else:
                return regular

# hahahahahahahah
@app.route("/brew")
def brew():
    return Response({'message': "I'm a teapot"}, status=418, mimetype='application/json')

#=====================|
#     NETWORKING.     |
#                     |
#=====================|

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    print(" * App secret key: " + str(app.secret_key))
    port = int(os.environ.get('PORT', config.app_port))
    app.run(host=config.app_host, port=port, debug=True)