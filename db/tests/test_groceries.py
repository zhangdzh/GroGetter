"""
Testing module for the groceries.py
"""
import pytest
import db.groceries as grocs
import db.groc_types as gtyp


def test_get_items():
    """
    tests get_items()
    """
    assert isinstance(grocs.get_items(), list)
    assert len(grocs.get_items()) > 0


def test_get_grocery_list():
    """
    tests get_grocery_list()
    """
    groc_list = grocs.get_grocery_list()
    assert isinstance(groc_list, dict)
    assert len(groc_list) > 0
    for item in groc_list:
        assert isinstance(item, str)
        assert isinstance(groc_list[item], dict)


def test_exists():
    """
    tests exists()
    """
    TEST_ITEM = "item1"
    assert grocs.exists(TEST_ITEM)


def test_get_details():
    """
    tests get_details()
    """
    TEST_GROCERY_NAME = "item1"
    assert isinstance(grocs.get_details(TEST_GROCERY_NAME), dict)
    for field in grocs.REQUIRED_FIELDS:
        assert field in grocs.get_details(TEST_GROCERY_NAME)


def test_get_types():
    """
    tests get_types()
    """
    assert isinstance(grocs.get_types(), list)
    assert len(grocs.get_types()) > 0
    for field in grocs.get_types():
        assert field in gtyp.GROC_TYPES


def test_add_and_remove_item():
    """
    tests add_item() and remove_item()
    """
    TEST_ITEM = "item2"
    TEST_GROCERY = {
        grocs.GROC_TYPE: gtyp.MISC,
        grocs.QUANTITY: 10,
        grocs.EXPIRATION_DATE: "10-20-2022"
    }
    grocs.add_item(TEST_ITEM, TEST_GROCERY)
    assert grocs.exists(TEST_ITEM)
    assert TEST_GROCERY == grocs.get_details(TEST_ITEM)
    grocs.remove_item(TEST_ITEM)
    assert not grocs.exists(TEST_ITEM)


def test_update_item():
    """
    tests update_item()
    """
    TEST_ITEM = "item1"
    TEST_GROCERY = {
        grocs.GROC_TYPE: gtyp.MISC,
        grocs.QUANTITY: 10,
        grocs.EXPIRATION_DATE: "10-20-2022"
    }
    grocs.update_item(TEST_ITEM, TEST_GROCERY)
    assert TEST_GROCERY == grocs.get_details(TEST_ITEM)


def test_update_quantity():
    """
    tests update_quantity()
    """
    TEST_ITEM = "item1"
    TEST_QUANTITY = 20
    grocs.update_quantity(TEST_ITEM, TEST_QUANTITY)
    assert TEST_QUANTITY == grocs.get_details(TEST_ITEM)[grocs.QUANTITY]