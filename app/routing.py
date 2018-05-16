#!/usr/bin/env python

"""
routing for lobe requests
"""


from flask import request

from messaging import fb_messenger

from constants import FB_ROUTE
from utils import *

from flask import Blueprint, render_template, abort

routes = Blueprint('simple_page', __name__,
                   template_folder='templates')


@routes.route('/', methods=['GET'])
def root():
    return '<html><p>Hello! Welcome to Lobe, unfortunately he has no frontend. </p></html>', 200


@routes.route(FB_ROUTE, methods=['GET'])
def fb_verify():
    return fb_messenger.webhook_verify()


@routes.route(FB_ROUTE, methods=['POST'])
def fb_post():
    log(request.json)
    if request.json: return fb_messenger.receive(request.json)
    return 'Incomplete Request', 400
