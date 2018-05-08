#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import requests
import logging
import json
import traceback


from sys import argv
from datetime import datetime
from flask import Flask, request, jsonify
from time import strftime
from logging.handlers import RotatingFileHandler



# user defined
from constants import *
from utils import log
import routing

from routing import routes

__author__ = "@realdavidawad"




def create_app(config_filename=None):
    app = Flask(__name__)
    app.register_blueprint(routes)
    return app

application = create_app()

# configure logger
logger = logging.getLogger('gunicorn.error')

# will happen before every request made to lobe.
#  @application.before_request
#  def before_request():
    #  return

#  @app.after_request
#  def after_request(response):
    #  """ Logging after every request. """
    #  # This avoids the duplication of registry in the log,
    #  # since that 500 is already logged via @app.errorhandler.
    #  if response.status_code != 500:
        #  ts = strftime('[%Y-%b-%d %H:%M]')
        #  logger.error('%s %s %s %s %s %s',
                      #  ts,
                      #  request.remote_addr,
                      #  request.method,
                      #  request.scheme,
                      #  request.full_path,
                      #  response.status)
    #  return response


#  @app.errorhandler(Exception)
#  def exceptions(e):
    #  """ Logging after every Exception. """
    #  ts = strftime('[%Y-%b-%d %H:%M]')
    #  tb = traceback.format_exc()
    #  logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
                  #  ts,
                  #  request.remote_addr,
                  #  request.method,
                  #  request.scheme,
                  #  request.full_path,
                  #  tb)
    #  return "Internal Server Error", 500



if __name__ == '__main__':

    # set logger
    application.logger.handlers.extend(gunicorn_error_logger.handlers)
    application.logger.setLevel(logging.DEBUG)
    #  application.logger.debug('this will show in the log')

    # maxBytes to small number, in order to demonstrate the generation of multiple log files (backupCount).
    handler = RotatingFileHandler('lobe.log', maxBytes=10000, backupCount=3)
    # getLogger(__name__):   decorators loggers to file + werkzeug loggers to stdout
    # getLogger('werkzeug'): decorators loggers to file + nothing to stdout
    # logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)
    logger.addHandler(handler)


    # run the server
    application.run(host = '0.0.0.0',
            port         = int(os.environ.get('PORT')),
            debug        = os.environ.get('DEBUG', False),
            use_reloader = True,
            threaded     = True)
