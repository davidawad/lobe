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
from users import User, UserList

USERS = UserList()


def determine_reply(current_user: User) -> str:
    """
    Takes current user object, gathers the users most recent message, and determines the reply
    :param User current_user: the user that sent the message

    """

    # get latest message
    most_recent_message = current_user.messages[-1]

    # send message to wit and classify intent
    parsed_intent = proc_wit.send_message(most_recent_message, current_user.client_id)

    # handle the parsed intent and create our response with it
    ret_text = extract_reply_from_intent(parsed_intent)

    return ret_text


def process_user_message(current_user: User) -> None:
    """
    procedure for new messages
    take the last message a user sent and send response for it
    :param User current_user: the user who sent the message
    """
    # TODO this could break down a bit when user sends more than one message
    # add user to list of users
    USERS.add_user(current_user)

    most_recent_message = current_user.messages[-1]

    if most_recent_message == 'TEST':
        # debugging mode, send request for location
        current_user.request_location()
        return

    if most_recent_message == 'STATUS':
        # TODO make bot give status report
        # debugging mode, send request for location
        current_user.send_text("HELLO MASTER.")
        current_user.send_text(str(USERS))
        return

    # determine reply with latest message
    reply_text = determine_reply(current_user)

    # in order for our bot to be realistic,
    # throttle slightly and send message in multiple sentences.
    sentences = proc_english.split_into_sentences(reply_text)

    current_user.converse(sentences)


def extract_reply_from_intent(parsed_intent):
    """
    Use the parsed intent from wit.ai and determine Lobe's response.
    :param str parsed_intent: the intent parsed from wit
    """
    ret_text = 'DEFAULT MESSAGE'

    # look at intent to determine if more work is necessary

    # handle greeting routine
    if parsed_intent == 'greetings':
        ret_text = GREETING

    elif parsed_intent in list(intent_message_key_mappings.keys()):
        # TODO use the intent to determine if we need state laws to answer the question
        # use the mapping dict to map the input to a proper basic response
        ret_text = intent_message_key_mappings.get(parsed_intent)

    else:
        ret_text = "I'm sorry I didn't understand that! Try again?"

    return ret_text


def user_location_update(user):
    """
    this routine defines what is done after the user passes a location
    """
    # reply to user with the state they're in
    response = 'Okay! So you live in ' + user.state + '.'
    response += 'What questions do you have?'
    user.send_text(response)
