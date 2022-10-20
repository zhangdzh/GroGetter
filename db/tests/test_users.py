"""
Testing module for users.py
"""

import pytest
import db.users as usr

def test_get_usernames():
    """
    tests get_usernames()
    """
    usrs = usr.get_usernames()
    assert isinstance(usrs, list)
    assert len(usrs) > 0