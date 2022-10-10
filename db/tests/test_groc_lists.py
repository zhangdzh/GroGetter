"""
Testing module for the groc_lists.py
"""
import pytest
from typing import Type
import db.groc_lists as glst

TEST_USER_NAME = 'user1'
USER_NAME = 'name'
LIST_NAME = 'list_name'
NUM_ITEMS = 'num_items'
GROC_LISTS = 'groc_lists'
REQUIRED_FIELDS = [USER_NAME, LIST_NAME, NUM_ITEMS, GROC_LISTS]


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


def test_add_wrong_username_type():
    with pytest.raises(TypeError):
        glst.add_groc(10, {})


def test_add_wrong_details_type():
    with pytest.raises(TypeError):
        glst.add_groc('new user list', [])


def test_add_missing_field():
    with pytest.raises(ValueError):
        glst.add_groc('new user list', {'foo': 'bar'})


def test_add_groc():
    details = {
        USER_NAME: TEST_USER_NAME,
        LIST_NAME: 'trip1',
        NUM_ITEMS: 1,
        GROC_LISTS: {
            'itemA': '10-20-2022'
        }
        }
    glst.add_groc(TEST_USER_NAME, details)
    assert glst.groc_lst_exists(TEST_USER_NAME)