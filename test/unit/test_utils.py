#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
unit tests for utils
"""
# add parent folders to system path to import classes to testing
import sys
sys.path.append('../')

# testing tools
from hypothesis import given, example
from hypothesis.strategies import text, floats

from nlp_tools.proc_english import split_into_sentences
from processing import determine_reply_from_intent
from utils import find_state_from_coords
from test_conf import *


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

    @given(floats(min_value=-180.00, max_value=180.00), floats(min_value=-180.00, max_value=180.00))
    def test_find_state(self, lat, long):
        """
        test for any coordinates
        """
        res = find_state_from_coords(lat, long)
        assert (isinstance(res, str) or res is None)

    @given(text())
    @example('')
    @example(None)
    def test_split_sentences(self, s):
        """
        split text should work for all strings
        """
        assert isinstance(split_into_sentences(s), list)
