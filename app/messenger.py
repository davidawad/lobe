#!/usr/bin/env python
# coding:utf-8

#  from __future__ import absolute_import
#  from __future__ import division
#  from __future__ import print_function
#  from __future__ import unicode_literals

import os
import sys
import requests
import json

from sys import argv
from wit import Wit
from flask import Flask, request
from datetime import datetime

from constants import *


# Wit.ai parameters
WIT_TOKEN = os.environ.get('WIT_TOKEN')
# Messenger API parameters
FB_PAGE_TOKEN = os.environ.get('FB_PAGE_TOKEN')
# A user secret to verify webhook get request.
FB_VERIFY_TOKEN = os.environ.get('FB_VERIFY_TOKEN')

# endpoint for facebook to send requests to
FB_ENDPOINT = '/fb_webhook'

# endpoint to send requests to
FB_MESSENGER_ENDPOINT = "https://graph.facebook.com/v2.6/me/messages"

app = Flask(__name__)

client = Wit(access_token=WIT_TOKEN)


@app.route(FB_ENDPOINT, methods=['GET'])
def messenger_webhook_verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == FB_VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route(FB_ENDPOINT, methods=['POST'])
def messenger_webhook():
    """
    Handler for webhook (currently for postback and messages)
    """
    data = request.json

    log("Facebook message received: " + str(data))

    if data.get('object') == 'page':

        log('data received!' + str(data['object']))

        for entry in data['entry']:

            log('examining entry' + str(entry))

            for messaging_event in entry["messaging"]:

                log('examining messaging_event:' + str(messaging_event))

                # get all the messages
                if messaging_event.get('message'):

                    # Yay! We got a new message!
                    # We retrieve the Facebook user ID of the sender
                    fb_id = messaging_event['sender']['id']
                    recipient_id = messaging_event["recipient"]["id"]

                    # We retrieve the message content
                    text = messaging_event["message"]["text"]

                    log("Received message: " +
                            text +
                            " from sender id: " +
                            fb_id)

                    # Let's forward the message to Wit /message
                    # and customize our response to the message in handle_message
                    response = client.message(msg=text, context={'session_id':fb_id})
                    handle_message(response=response, fb_id=fb_id)
                    # TODO should this function return anything
    else:
        # Returned another event
        log('Received an invalid message on the facebook endpoint: ' + data)
        # TODO return a different error code on error

    return 'OK', 200



#TODO write something to break apart shorter replies
def fb_message(sender_id, text):
    """
    Function for returning response to messenger
    """
    data = {
        'recipient': {'id': sender_id},
        'message': {'text': text}
    }
    # Setup the query string with your PAGE TOKEN
    qs = 'access_token=' + FB_PAGE_TOKEN
    # Send POST request to messenger
    resp = requests.post('https://graph.facebook.com/me/messages?' + qs,
                         json=data)
    return resp.content


def send_content(recipient_id, content):

    log("sending message to {recipient}: {content}".format(
        recipient=recipient_id,
        content=str(content)))

    params = {
        "access_token": FB_PAGE_TOKEN
    }

    headers = {
        "Content-Type": "application/json"
    }

    # update data with json formatted passed content
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": content
    })

    r = requests.post(FB_MESSENGER_ENDPOINT,
                        params=params,
                        headers=headers,
                        data=data)

    if r.status_code != 200:
        log(r.status_code)
        log(r)


def handle_parsed_intent(parsed_intent):
    """
    Determine the response and properly format it
    """
    ret_obj = {}
    ret_text, ret_replies, ret_buttons = 'DEFAULT MESSAGE', [], []

    # TODO look at intent to determine if more work is necessary
    log('RECEIVED PARSED INTENT: ' + str(parsed_intent))

    # handle greeting routine
    if parsed_intent == 'greetings':
        ret_text = "Hello! My name is Lobe, I'm a robot designed to help you, but I'm not an attorney! Any information I give is exclusively for entertainment purposes only."

    elif parsed_intent in list(intent_message_key_mappings.keys()):
        # use the mapping dict to map the input to a proper basic response
        ret_text = intent_message_key_mappings.get(parsed_intent)

    else:
        ret_text = "I'm sorry I didn't understand that! Try again?"


    # stitch together the return object
    # TODO cleaner way to do this setting?
    ret_obj["text"] = ret_text

    if ret_replies:
        ret_obj["quick_replies"] = ret_replies

    if ret_buttons:
        ret_obj["buttons"] = ret_buttons

    return ret_obj


def first_entity_value(entities):
    """
    Returns first entity value
    """
    log("Entities " + str(entities))

    ret = ''

    if not entities:
        log("Entities object is none")
        return None

    # we can have any intent here so use a list comp to find the highest confidence, of all possible intents that wit could return to us
    largest_confidence_per_entity = [ max(entities[entity], key=lambda x: x['confidence']) for entity in list(entities.keys())]

    log('largest confidence entities: ' + str(largest_confidence_per_entity))

    # find the largest confidence overall
    largest_confidence_object = max(largest_confidence_per_entity, key=lambda x: x['confidence'])

    log('largest confidence object: ' + str(largest_confidence_object))

    for entity in list(entities.keys()):
        if largest_confidence_object in entities.get(entity):

            # get information for our specific entity
            log('most likely entity found: ' + str(entity))

            if entity == 'greetings':
                log('ENTITY IS GREETINGS')
                ret = 'greetings'

            if entity == 'intent':
                log('ENTITY IS AN INTENT')
                ret = largest_confidence_object['value']

    log('returning parsed intent: ' + str(ret))

    return ret


def handle_message(response, fb_id):
    """
    Customizes our response to the message and sends it
    """
    log("RESPONSE: " + str(response))

    entities = response.get('entities')

    # Checks if user's message is a greeting
    # Otherwise we will just repeat what they sent us
    parsed_intent = first_entity_value(entities)

    # handle the parsed intent and create our response
    response_object = handle_parsed_intent(parsed_intent)

    # TODO parse intent to craft message
    # use this for basic legal info
    # http://www.18thjudicialcircuitpublicdefender.com/client-information/

    log('SENDING MESSAGE: ' + str(response_object))

    # send message
    #  fb_message(fb_id, text)
    send_content(fb_id, response_object)


def log(msg):
    """
    simple wrapper for logging to stdout on heroku
    """
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        print ("{}".format(str(msg)))
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()


if __name__ == '__main__':
    # Run Server
    app.run(host='0.0.0.0',
            port=int(os.environ.get('PORT')),
            debug=os.environ.get('DEBUG'))
