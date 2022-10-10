"""
Testing module for the groc_lists.py
"""

import db.groc_lists as glst

USER_NAME = 'name'
LIST_NAME = 'list_name'
NUM_ITEMS = 'num_items'
GROC_LISTS = 'groc_lists'
REQUIRED_FIELDS = [USER_NAME, LIST_NAME, NUM_ITEMS, GROC_LISTS]

TEST_USER_NAME = 'user1'

def test_get_usernames():
    """
    tests get_usernames()
    """
    assert isinstance(glst.get_usernames(), list)


def test_get_details():
    """
    tests get_details()
    """
    assert isinstance(glst.get_details(TEST_USER_NAME), dict)
    for field in REQUIRED_FIELDS:
        assert field in glst.get_details(TEST_USER_NAME)