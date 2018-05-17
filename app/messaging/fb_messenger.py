#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
facebook messenger adapter
"""

import os
import json

import requests
from flask import request

import processing
from utils import log
from users import User


# Messenger API parameters
FB_PAGE_TOKEN = os.environ.get('FB_PAGE_TOKEN')
# A user secret to verify webhook get request.
FB_VERIFY_TOKEN = os.environ.get('FB_VERIFY_TOKEN')

# endpoint to send requests to
FB_MESSENGER_ENDPOINT = "https://graph.facebook.com/v2.6/me/messages"


def webhook_verify():
    """
    webhook verification for facebook messenger API
    """
    log("Received verification request from fb.")
    # when the server side endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == FB_VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


def receive(data):
    """
    Handler for webhook (currently for postback and messages)
    Parses out the message and bubbles it up to the processing layer
    """

    log("Facebook message received: " + str(data))

    if data.get('object') == 'page':

        log('Page data received!' + str(data['object']))

        for entry in data.get('entry', None):

            log('Examining entry :' + str(entry))

            for messaging_event in entry.get("messaging", None):

                log('Examining messaging_event:' + str(messaging_event))

                # get all the messages
                if messaging_event.get('message', False):

                    # Yay! We got a new message!
                    # We retrieve the Facebook user ID of the sender
                    fb_id = messaging_event['sender']['id']

                    # create new user object, bubble it up along with their message
                    current_user = User('fb', fb_id)

                    message = messaging_event.get('message')
                    #  attachments = message.get('attachments', None)

                    coords = [m.get("attachments", {}).get("payload", {}).get("coords") for m in [message]][0]

                    print("COORDS")
                    print(coords)
                    log(coords)



                    #  attachments = None
                    #  payload = None
                    #  coords = None

                    #  if attachments:
                        #  payload = attachments.get('payload', None)

                    #  if payload:
                        #  coords = attachments.get('coordinates', None)

                    if coords:
                        print("ADDING COORDINATES")
                        coords = attachments['payload']['coordinates']
                        print(coords)
                        lat = coords["lat"]
                        long = coords["long"]
                        current_user.add_coordinates(lat, long)

                    # We retrieve the message content
                    text = messaging_event["message"]["text"]

                    log("Received message: " +
                        text +
                        " from sender id: " +
                        fb_id)

                    # append latest message to user object
                    current_user.append_message(text)

                    # create or find the user object, bubble user up to processing
                    processing.process_user_message(current_user)

    else:
        # Returned another event
        log('Received an invalid message on the facebook endpoint: ' + data)
        return 'Server Error', 500

    return 'OK', 200


def request_location(fb_id):
    """
    Sends a request for location to facebook using the fb_id
    """

    # used to request location in messenger
    # https://developers.facebook.com/docs/messenger-platform/send-messages/quick-replies#locations
    location_request_object = {"content_type": "location"}

    response_object = format_message('What state are you in? Share your location?', location_request_object)
    send_content(fb_id, response_object)


def send_text(send_to_id, text):
    """
    Send out message to a messenger user.
    Just a higher level interface that only needs a string.
    """
    response_object = format_message(text)
    send_content(send_to_id, response_object)


def format_message(ret_text, ret_replies=None, ret_buttons=None):
    """
    Stitch together the return object based on whatever response text has been selected.
    Returns formatted object so that it can be passed to send_content.
    """
    if not ret_replies:
        ret_replies = []

    if not ret_buttons:
        ret_buttons = []

    ret_obj = {}

    ret_obj["text"] = ret_text

    if ret_replies:
        ret_obj["quick_replies"] = ret_replies

    if ret_buttons:
        ret_obj["buttons"] = ret_buttons

    return ret_obj


def send_content(recipient_id, content):
    """
    Takes a messenger formatted object and sends it to the specified recepient
    """
    log("Sending message to {recipient}: {content}".format(
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

    request_object = requests.post(FB_MESSENGER_ENDPOINT,
                                   params=params,
                                   headers=headers,
                                   data=data)

    if request_object.status_code != 200:
        log(request_object)
