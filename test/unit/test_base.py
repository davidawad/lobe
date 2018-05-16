# -*- coding: utf-8 -*-
"""
unit tests
"""

# add parent folders to system path to import classes to testing
import sys
sys.path.append('../')

from test_conf import *

from processing import handle_parsed_intent
from nlp_tools.proc_english import split_into_sentences


class TestBotProcessor(object):
    """ Unit Tests for Processing Module

    """

    def test_handle_parsed_intent(self):
        response_text = handle_parsed_intent("greetings")
        assert response_text == "Hello! My name is Lobe, I'm a robot designed to help you, but I'm not an attorney! Any information I give is exclusively for entertainment purposes only."

        return


    def test_handle_parsed_intent(self):
        response_text = handle_parsed_intent("court_basics")
        assert "You will appear before" in response_text

        return


    def test_handle_parsed_intent_bad_input(self):
        response_text = handle_parsed_intent(None)
        assert "I'm sorry I didn't understand that!" in response_text
        return

    def test_handle_parsed_intent_bad_input(self):
        response_text = handle_parsed_intent('FAKEFAKE')
        assert "I'm sorry I didn't understand that!" in response_text
        return


class TestBotNLP(object):

    """ Unit Tests for NLP tools module

    """
    def test_handle_parsed_intent(self):
        sentences = split_into_sentences("Hello! My name is Lobe, I'm a robot designed to help you, but I'm not an attorney! Any information I give is exclusively for entertainment purposes only.")

        assert sentences == ['Hello!', "My name is Lobe, I'm a robot designed to help you, but I'm not an attorney!", 'Any information I give is exclusively for entertainment purposes only.']

        return

