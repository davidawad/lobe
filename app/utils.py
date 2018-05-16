#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
contains some convenience functions
"""
import os
import sys
import json
import flask
import logging


DEBUG = os.environ.get('DEBUG', False)


logger = logging.getLogger('gunicorn.error')

#  application.logger.debug('this will show in the log')


def log(msg):
    """
    simple wrapper for logging to stdout on heroku
    """
    if not DEBUG: pass
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        formatted_msg = "{}".format(str(msg))
        print(formatted_msg)
        # logger doesn't work
        logger.debug(formatted_msg)
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    # sys.stdout.flush()
