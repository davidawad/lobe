#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
unit tests for utils
"""

# add parent folders to system path to import classes to testing
import sys
sys.path.append('../')

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

    # def test_find_state(self):

    #  @fixture(scope='function')
    #  def stuff():
        #  global counter
        #  counter = 0


    #  @given(a=st.none())
    #  def test_stuff(a, stuff):
        #  global counter
        #  counter += 1
        #  assert counter == 1


