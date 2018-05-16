#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
base python module for importing other modules to be used in tests
"""

import sys
import pytest

# add parent folders to system path to import classes to testing
sys.path.append('../app')

from server import create_app


@pytest.fixture(scope='module')
def new_user():
    """
    creates a new user, currently skeleton code
    """
    return


@pytest.fixture(scope='module')
def test_client():
    """
    builds a test flask client to run functional tests against
    """
    flask_app = create_app()

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()
    return


@pytest.fixture(scope='module')
def init_database():
    """
    initializes database structures, probably not necessary, skeleton code.
    """
    return

