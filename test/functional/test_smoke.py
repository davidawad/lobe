# -*- coding: utf-8 -*-
import pytest

# add parent folders to system path to import classes to testing
import sys
sys.path.append('../')

from test_conf import *



# smoke tests
class TestForSmoke(object):

    def test_something_basic(self):
        pass
