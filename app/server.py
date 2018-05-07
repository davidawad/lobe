#!/usr/bin/env python
# coding:utf-8

import os
import sys
import requests
import json

from sys import argv
from datetime import datetime
from flask import Flask, request

from messaging.fb_messenger import fb_messenger_router

from constants import *

application = Flask(__name__)

application.register_blueprint(fb_messenger_router, url_prefix=FB_ROUTE)




# route to the root directory
@application.route('/')
def home():
    return '<p>Lobe currently has no frontend. Thanks!<p>', 200


# will happen before every request made to lobe,
# currently just passes it along
@application.before_request
def before_request():
    return


def log(msg):
    """
    simple wrapper for logging to stdout on heroku
    """
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        print ("{}".format(str(msg)))
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()



if __name__ == '__main__':
    # run the server
    application.run(host = '0.0.0.0',
            port         = int(os.environ.get('PORT')),
            debug        = os.environ.get('DEBUG'),
            use_reloader = True,
            threaded     = True)
