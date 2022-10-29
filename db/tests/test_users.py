"""
Testing module for users.py
"""

import pytest
import db.users as usr

TEST_USER_NAME = 'user1'
TEST_PW = "helloworld"


def test_add_user():
    """
    tests add_user()
    """
    details = {}
    details[usr.USER_NAME] = usr.TEST_USER_NAME
    details[usr.EMAIL] = usr.TEST_EMAIL
    details[usr.PASSWORD] = usr.TEST_PASSWORD
    usr.add_user(usr.TEST_USER_NAME, details)


def test_get_usernames():
    """
    tests get_usernames()
    """
    usrs = usr.get_usernames()
    assert isinstance(usrs, list)
    assert len(usrs) > 1


def test_get_users_dict():
    usrs = usr.get_users_dict()
    assert isinstance(usrs, dict)
    assert len(usrs) > 1

    
def test_get_user_email():
    """
    tests get_user_email()
    """
    email = usr.get_user_email(TEST_USER_NAME)
    assert isinstance(email, str)


def test_get_user_password():
    """
    tests get_user_password()
    """
    password = usr.get_user_password(TEST_USER_NAME)
    assert isinstance(password, str)


def test_change_password():
    """
    tests change_password()
    """
    usr.change_password(TEST_USER_NAME, TEST_PW)    
