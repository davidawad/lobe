# -*- coding: utf-8 -*-
"""
Smoke tests to ensure application has basic functionality
"""

# add parent folders to system path to import classes to testing
import sys
sys.path.append('../')

from test_conf import *


def test_home_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Welcome to Lobe' in response.data
