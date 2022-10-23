"""
Testing module for users.py
"""

import pytest
import db.users as usr


def test_add_user():
    """
    tests add_user()
    """
    details = {}
    details[usr.USER_NAME] = usr.TEST_USER_NAME
    details[usr.EMAIL] = usr.TEST_EMAIL
    usr.add_user(usr.TEST_USER_NAME, details)


def test_get_usernames():
    """
    tests get_usernames()
    """
    usrs = usr.get_usernames()
    assert isinstance(usrs, list)
    assert len(usrs) > 1
