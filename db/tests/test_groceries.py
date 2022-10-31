"""
Testing module for the groceries.py
"""
import pytest
import db.groceries as grocs


def test_get_grocery_items():
    """
    tests get_grocery_items()
    """
    assert isinstance(grocs.get_grocery_items(), list)
    assert len(grocs.get_grocery_items()) > 0
