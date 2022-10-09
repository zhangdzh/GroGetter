"""
Testing module for the groc_lists.py
"""

import db.groc_lists as glst


USER_NAME = 'user1'

def test_get_usernames():
    """
    tests get_usernames()
    """
    assert isinstance(glst.get_usernames(), list)


def test_get_details():
    """
    tests get_details()
    """
    assert isinstance(glst.get_details(USER_NAME), list)
