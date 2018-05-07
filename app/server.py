#!/usr/bin/env python
# coding:utf-8

import os
import sys
import requests
import logging
import json

from sys import argv
from datetime import datetime
from flask import Flask, request

#  from messaging.fb_messenger import fb_messenger_router
from messaging import fb_messenger_router

from constants import *

application = Flask(__name__)


application.register_blueprint(fb_messenger_router,
                               url_prefix=FB_ROUTE)


gunicorn_error_logger = logging.getLogger('gunicorn.error')
application.logger.handlers.extend(gunicorn_error_logger.handlers)
application.logger.setLevel(logging.DEBUG)
application.logger.debug(fb_messenger_router)


#  @application.route('/', methods=['GET'])
#  def home():
    #  return messaging.fb_messenger.messenger_webhook_verify()

# route to the root directory
#  @application.route('/')
#  def home():
    #  application.logger.debug('FUCK ALL LIFE')
    #  return '<p>Lobe currently has no frontend. Thanks!<p>', 200


# will happen before every request made to lobe,
# currently just passes it along
#  @application.before_request
#  def before_request():
    #  return


#  import logging
#  # set up gunicorn logger
#  gunicorn_error_logger = logging.getLogger('gunicorn.error')
#  app.logger.handlers.extend(gunicorn_error_logger.handlers)
#  app.logger.setLevel(logging.DEBUG)
#  app.logger.debug('this will show in the log')

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
