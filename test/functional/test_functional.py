# -*- coding: utf-8 -*-
import pytest

# add parent folders to system path to import classes to testing
import sys
sys.path.append('../')

import json

from test_conf import *


def test_verification(test_client):
    """
    ensure that fb webhook registers successfully
    """
    response = test_client.get('/messaging/fb_messenger')
    assert response.status_code == 200
    assert b'Hello world' in response.data


def test_route_put(test_client):
    """
    ensure that fb webhook doesn't respond
    """
    response = test_client.put('/messaging/fb_messenger')
    assert response.status_code == 405
    assert b'Not Allowed' in response.data


def test_route_delete(test_client):
    """
    ensure that fb webhook doesn't respond
    """
    response = test_client.delete('/messaging/fb_messenger')
    assert response.status_code == 405
    assert b'Not Allowed' in response.data


def test_fb_message_response_null_input(test_client):
    """
    ensure that fb message webhook fails when used without data
    """
    response = test_client.post('/messaging/fb_messenger')

    assert response.status_code == 400
    assert b'Incomplete Request' in response.data


def test_fb_message_response(test_client):
    """
    ensure that fb webhook registers successfully
    """

    data_segment = {
        "object": "page",
        "entry": [{
                "id": "779879168810137",
                "time": 1525712604698,
                "messaging": [{
                        "sender": {
                                "id": "1019000991512235"
                        },
                        "recipient": {
                                "id": "779879168810137"
                        },
                        "timestamp": 1525712604506,
                        "message": {
                                "mid": "mid.$cAALFS4nhWAlpbNQVWljO47fxUCdE",
                                "seq": 1369896,
                                "text": "hi"
                        }
                }]
        }]
    }

    response = test_client.post('/messaging/fb_messenger', json=data_segment)

    assert response.status_code == 200
    assert b'OK' in response.data
