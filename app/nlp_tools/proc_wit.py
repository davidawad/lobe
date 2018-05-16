#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
drivers for wit.ai
"""
import os

import wit

from utils import log

# Wit.ai parameters
WIT_TOKEN = os.environ.get('WIT_TOKEN')

client = wit.Wit(access_token=WIT_TOKEN)


def send_message(msg, id_tag):
    """
    Takes a message and a unique id for wit to identify the conversation
    returns a parsed intent value using wit's filters
    """

    response = client.message(msg=msg, context={'session_id': id_tag})

    entities = response.get('entities')

    # Checks if user's message is a greeting
    parsed_intent = first_entity_value(entities)

    return parsed_intent


def first_entity_value(entities):
    """
    Returns first entity value
    """
    log("Entities " + str(entities))

    ret = ''

    if not entities:
        log("Entities object is none")
        return None

    # we can have any intent here
    # so use a list comp to find the highest confidence,
    # of all possible intents that wit could return to us
    largest_confidence_per_entity = [max(entities[entity], key=lambda x: x['confidence']) for entity in list(entities.keys())]

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
