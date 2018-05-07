
def handle_text_message(text):
    """
    Takes input message text and determines the response
    """
    response_text = "TEXT FROM handle_text_message()"

    return response_text


# NOTE: here 'response' is actually the message sent by the user
def handle_fb_message(text, fb_id):
    """
    Customizes our response to the message and sends it
    """
    log("RESPONSE: " + str(response))


    response = client.message(msg=text, context={'session_id':fb_id})

    # handle_message(response=response, fb_id=fb_id)

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




def handle_parsed_intent(parsed_intent):
    """
    Use the parsed intent from wit.ai and format it for fb
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


