#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
middleware processing of messages and sending them to correct clients
"""
import math
import time

from constants import intent_message_key_mappings, GREETING
from utils import log

from nlp_tools import proc_wit, proc_english
from messaging import fb_messenger


def handle_text_message(text):
    """
    Takes input message text and determines the response, gives it back to the caller

    Currently basically a skeleton
    """
    response_text = "sample text from skeleton function"
    return response_text


def handle_fb_message(text, fb_id):
    """
    Handler for fb messages
    """

    # send message to wit
    parsed_intent = proc_wit.send_message(text, fb_id)

    # handle the parsed intent and create our response
    ret_text = handle_parsed_intent(parsed_intent)

    # in order for our bot to be realistic,
    # throttle slightly and send message in multiple sentences.
    sentences = proc_english.split_into_sentences(ret_text)

    for _ in sentences:
        # sleep for some amount of time that makes sense based on length of message
        time.sleep(max((math.log(len(_)) - 3), 0))
        fb_messenger.send_text(fb_id, _)

    return


def handle_parsed_intent(parsed_intent):
    """
    Use the parsed intent from wit.ai and determine Lobe's response.
    """
    ret_text = 'DEFAULT MESSAGE'

    # look at intent to determine if more work is necessary
    log('RECEIVED PARSED INTENT: ' + str(parsed_intent))

    # handle greeting routine
    if parsed_intent == 'greetings':
        ret_text = GREETING

    elif parsed_intent in list(intent_message_key_mappings.keys()):
        # use the mapping dict to map the input to a proper basic response
        ret_text = intent_message_key_mappings.get(parsed_intent)

    else:
        ret_text = "I'm sorry I didn't understand that! Try again?"

    return ret_text
