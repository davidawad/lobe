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
from flask import Flask, request, Blueprint, jsonify
from datetime import datetime

from constants import *


# Messenger API parameters
FB_PAGE_TOKEN = os.environ.get('FB_PAGE_TOKEN')
# A user secret to verify webhook get request.
FB_VERIFY_TOKEN = os.environ.get('FB_VERIFY_TOKEN')

# endpoint to send requests to
FB_MESSENGER_ENDPOINT = "https://graph.facebook.com/v2.6/me/messages"

# handles all I/O with facebook messenger.
# designed to be used with a facebook page.

# takes messages and sends out messages.
# simple as that

# set up blueprint for fb_messenger
fb_messenger_router = Blueprint('fb_messenger', __name__)


@fb_messenger_router.route(FB_ROUTE, methods=['GET'])
def messenger_webhook_verify():
    # when the server side endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == FB_VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200



@fb_messenger_router.route(FB_ROUTE, methods=['GET', 'POST'])
def receive():
    """
    Handler for webhook (currently for postback and messages)
    Parses out the message and bubbles it up to the processing layer
    """
    data = request.json

    log("Facebook message received: " + str(data))

    if data.get('object') == 'page':

        log('Page data received!' + str(data['object']))

        for entry in data['entry']:

            log('Examining entry :' + str(entry))

            for messaging_event in entry["messaging"]:

                log('Examining messaging_event:' + str(messaging_event))

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


                    # TODO PROCESS TEXT
                    processing.handle_fb_message(text, fb_id)

                    # response = client.message(msg=text, context={'session_id':fb_id})
                    # handle_message(response=response, fb_id=fb_id)

                    # TODO WHEN TEXT IS GIVEN BACK TAKE REPLY AND SEND IT OUT

                    # TODO should this function return anything HERe?
    else:
        # Returned another event
        log('Received an invalid message on the facebook endpoint: ' + data)
        # TODO more structured mechanism for this
        return 'Server Error', 500

    return 'OK', 200
    pass



# TODO(me@davidawad.com) write something to break apart long paragraphs into shorter replies.
# Not sure if that should be done at the I/O level or whether it makes more sense at the processing level
def send_text(sender_id, text):
  """
  Send out reply to a messenger user.
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
    """
    Send out messenger buttons or content to a messenger user.
    """
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
