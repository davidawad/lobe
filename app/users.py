#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import time

import utils
from messaging import fb_messenger


"""
lightweight user management module
"""


class User:  # pylint: disable=too-few-public-methods
    """
    simple user class, tracks some basics about chatbot users
    """

    def __init__(self, client: str, client_id: str):
        """
        setup
        """
        self.client = client
        self.client_id = client_id

        self.lat = None
        self.long = None
        # lobe assumes his clients are all in the US
        self.state = None  # NJ for example
        # create array to track our messages
        self.messages = []

    def __str__(self):
        """
        string method for simplicity
        """
        return str(self.__dict__)

    def __eq__(self, other):
        """
        enables userA == userB
        """
        return self.__dict__ == other.__dict__

    def append_message(self, msg: str):
        """
        tracks our messages from the user, append only
        """
        if not isinstance(msg, str):
            raise ValueError("append message given a non string: " + str(msg))
        self.messages.append(msg)

    def converse(self, messages):
        """
        take array of strings and send them to the user
        with a time delay to make them more realistic
        """
        if not messages:
            raise ValueError('user.converse given nothing')

        for _ in messages:
            # sleep for some amount of time as
            # function of message length
            # delay = log(length of message) - 3
            delay = max((math.log(len(_)) - 3), 0)
            time.sleep(delay)
            self.send_text(_)

    def send_text(self, text: str) -> None:
        """
        take string and send it to the user
        :param str the text to send to the user with the correct adapter
        """
        if self.client == 'fb':
            fb_messenger.send_text(self.client_id, text)

    def request_location(self) -> None:
        """
        requests location of user
        """
        if self.client == 'fb':
            fb_messenger.request_location(self.client_id)

    def add_coordinates(self, lat, long) -> None:
        """
        sets latitude and longitude of user, and then determines what US state the user is in
        """
        self.lat = lat
        self.long = long

        self.state = utils.find_state_from_coords(lat, long)


class UserList:
    """
    module that maintains list of users
    """

    def __init__(self):
        self.users = []

    def add_user(self, user_object: User) -> None:
        """
        adds user if they don't exist
        """
        if user_object not in self.users:
            self.users.append(user_object)

    def find_user(self, client_id: str) -> User:
        """
        finds user object by 'client_id'
        """
        ret = None
        for _ in self.users:
            if _.client_id == client_id:
                ret = _
        return ret

    def remove_user(self, user_object: User) -> None:
        """
        removes a user if they exist
        """
        if not self.find_user(user_object):
            return
        self.users.remove(user_object)

    def reset(self) -> None:
        self.users = []




