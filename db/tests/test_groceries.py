"""
Testing module for the groceries.py
"""
import pytest
import db.groceries as grocs
import db.groc_types as gtyp

TEST_GROCERY_NAME = "item1"
TEST_GROCERY = {
    grocs.GROC_TYPE: gtyp.BAKED_GOODS,
    grocs.Quantity: "10",
    grocs.EXPIRATION_DATE: "10-20-2022"
}


def test_get_grocery_items():
    """
    tests get_grocery_items()
    """
    assert isinstance(grocs.get_grocery_items(), list)
    assert len(grocs.get_grocery_items()) > 0


def test_get_grocery_details():
    """
    tests get_grocery_details()
    """
    assert isinstance(grocs.get_grocery_details(TEST_GROCERY_NAME), dict)
    for field in grocs.REQUIRED_FIELDS:
        assert field in grocs.get_grocery_details(TEST_GROCERY_NAME)