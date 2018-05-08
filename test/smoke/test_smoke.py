# -*- coding: utf-8 -*-
import pytest

# add parent folders to system path to import classes to testing
import sys
sys.path.append('../')

from test_conf import *


# sample fb request

#  {'object': 'page', 'entry': [{'id': '779879168810137', 'time': 1525712604698, 'messaging': [{'sender': {'id': '1019000991512235'}, 'recipient': {'id': '779879168810137'}, 'timestamp': 1525712604506, 'message': {'mid': 'mid.$cAALFS4nhWAlpbNQVWljO47fxUCdE', 'seq': 1369896, 'text': 'hi'}}]}]}



# smoke tests
def test_home_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Welcome to Lobe' in response.data

