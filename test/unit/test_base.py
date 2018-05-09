# -*- coding: utf-8 -*-

import pytest

# add parent folders to system path to import classes to testing
import sys
sys.path.append('../')

from test_conf import *

from processing import handle_parsed_intent
from nlp_tools.proc_english import split_into_sentences

def return_response_object(text, quick_replies=None, buttons=None):
    ret_obj = {}
    ret_obj['text'] = text
    ret_obj['quick_replies'] = quick_replies
    ret_obj['buttons'] = buttons
    return ret_obj


class TestBotUtils(object):

    def test_intro_message_response(self):
        #  reply = bot_response("Hello")
        #  response_obj = return_response_object("Hello! I’m Sloan, your automated guide for advice on your student loans brought to you by TISLA. This is not legal advice but simple guidance to help you manage your student loan debt. Send 'restart' at any time to restart. Ready? Simply type your question and I’ll try and guide you to the best way to manage your student debt!", raw_response_data['replies']['intro'])

        #  assert reply.get('text', None) == response_obj.get('text')
        #  assert reply.get('buttons', None) == response_obj.get('buttons')
        #  assert reply.get('quick_replies', None) == response_obj.get('quick_replies')
        return



class TestBotProcessor(object):

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

    def test_handle_parsed_intent(self):
        sentences = split_into_sentences("Hello! My name is Lobe, I'm a robot designed to help you, but I'm not an attorney! Any information I give is exclusively for entertainment purposes only.")

        assert sentences == ['Hello!', "My name is Lobe, I'm a robot designed to help you, but I'm not an attorney!", 'Any information I give is exclusively for entertainment purposes only.']

        return

