#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
unit tests for utils
"""

# add parent folders to system path to import classes to testing
import sys
sys.path.append('../')

from test_conf import *

from processing import extract_reply_from_intent
from nlp_tools.proc_english import split_into_sentences

from utils import find_state_from_coords




class TestUtils(object):
    """
    Unit Tests for Utils
    """

    def test_find_state(self):
        """
        basic test for CA coordinates
        """
        assert find_state_from_coords(37.483872693672, -122.14900441942) == 'CA'
        assert find_state_from_coords(40.483872693672, -73.9321059) == 'NY'


