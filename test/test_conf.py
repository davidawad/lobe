# -*- coding: utf-8 -*-
import pytest

# add parent folders to system path to import classes to testing
import sys
sys.path.append('../app')

from server import *

#  from project import create_app, db
#  from project.models import User


@pytest.fixture(scope='module')
def new_user():
    #  user = User('patkennedy79@gmail.com', 'FlaskIsAwesome')
    return
    #  return user


@pytest.fixture(scope='module')
def test_client():
    #  flask_app = create_app('flask_test.cfg')

    #  # Flask provides a way to test your application by exposing the Werkzeug test Client
    #  # and handling the context locals for you.
    #  testing_client = flask_app.test_client()

    #  # Establish an application context before running the tests.
    #  ctx = flask_app.app_context()
    #  ctx.push()

    #  yield testing_client  # this is where the testing happens!

    #  ctx.pop()
    return


@pytest.fixture(scope='module')
def init_database():
    # Create the database and the database table
    #  db.create_all()

    #  # Insert user data
    #  user1 = User(email='patkennedy79@gmail.com', plaintext_password='FlaskIsAwesome')
    #  user2 = User(email='kennedyfamilyrecipes@gmail.com', plaintext_password='PaSsWoRd')
    #  db.session.add(user1)
    #  db.session.add(user2)

    #  # Commit the changes for the users
    #  db.session.commit()

    #  yield db  # this is where the testing happens!

    #  db.drop_all()
    return

