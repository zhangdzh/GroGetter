"""
Testing module for the groceries.py
"""
import pytest
import os
import db.groceries as grocs
import db.groc_types as gtyp

NEW_GROC_NAME = "test"
NEW_GROC_DETAILS = {
                    grocs.GROC_TYPE: "Carbs",
                    grocs.QUANTITY: 2,
                    grocs.EXPIRATION_DATE: "10-31-2024"
                    }

RUNNING_ON_CICD_SERVER = os.environ.get('CI', False)


@pytest.fixture(scope='function')
def new_groc_item():
    grocs.add_item(NEW_GROC_NAME, NEW_GROC_DETAILS)
    yield
    grocs.remove_item(NEW_GROC_NAME)


def test_get_items():
    """
    tests get_items()
    """
    assert isinstance(grocs.get_items(), list)
    assert len(grocs.get_items()) > 0

@pytest.mark.skip("Can't run this test untill the we figure out MongoDB Connection.")
# gives pymongo.errors.ServerSelectionTimeoutError
def test_get_grocery_list():
    """
    tests get_grocery_list()
    """
    '''
    groc_list = grocs.get_grocery_list()
    assert isinstance(groc_list, dict)
    assert len(groc_list) > 0
    for item in groc_list:
        assert isinstance(item, str)
        assert isinstance(groc_list[item], dict)
    '''
    if not RUNNING_ON_CICD_SERVER:
        groceries = grocs.get_grocery_list()
        assert isinstance(groceries, dict)
        # length later - perhaps after adding fixture to create new
        # note: dict currently empty?


def test_exists(new_groc_item):
    """
    tests exists()
    """
    assert grocs.exists(NEW_GROC_NAME)


def test_get_details(new_groc_item):
    """
    tests get_details()
    """
    assert isinstance(grocs.get_details(NEW_GROC_NAME), dict)
    for field in grocs.REQUIRED_FIELDS:
        assert field in grocs.get_details(NEW_GROC_NAME)


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


def test_update_item(new_groc_item):
    """
    tests update_item()
    """
    # TEST_ITEM = "item1"
    TEST_GROCERY = {
        grocs.GROC_TYPE: gtyp.MISC,
        grocs.QUANTITY: 10,
        grocs.EXPIRATION_DATE: "10-20-2022"
    }
    grocs.update_item(NEW_GROC_NAME, TEST_GROCERY)
    assert TEST_GROCERY == grocs.get_details(NEW_GROC_NAME)


def test_raised_exceptions_for_add_item():
    """
    tests raised exceptions for add_item()
    """
    TEST_GROCERY = {
        grocs.GROC_TYPE: gtyp.MISC,
        grocs.QUANTITY: 10,
        grocs.EXPIRATION_DATE: "10-20-2022"
    }
    TEST_ITEM = 1
    with pytest.raises(TypeError):
        grocs.add_item(TEST_ITEM, TEST_GROCERY)
    TEST_ITEM = "item1"
    with pytest.raises(ValueError):
        grocs.add_item(TEST_ITEM, TEST_GROCERY)
    TEST_ITEM = "item2"
    TEST_GROCERY[grocs.GROC_TYPE] = "invalid"
    with pytest.raises(ValueError):
        grocs.add_item(TEST_ITEM, TEST_GROCERY)
    TEST_GROCERY = {
        grocs.QUANTITY: 10,
        grocs.EXPIRATION_DATE: "10-20-2022"
    }
    with pytest.raises(KeyError):
        grocs.add_item(TEST_ITEM, TEST_GROCERY)


def test_update_quantity(new_groc_item):
    """
    tests update_quantity()
    """
    # TEST_ITEM = "item1"
    TEST_QUANTITY = 20
    grocs.update_quantity(NEW_GROC_NAME, TEST_QUANTITY)
    assert TEST_QUANTITY == grocs.get_details(NEW_GROC_NAME)[grocs.QUANTITY]


def test_add_item_dup(new_groc_item):
    with pytest.raises(ValueError):
        grocs.add_item(NEW_GROC_NAME, NEW_GROC_DETAILS)


def test_groc_lst_not_exists():
    assert not grocs.exists('Some nonsense list')


def test_add_wrong_name_type():
    with pytest.raises(TypeError):
        grocs.add_item(7, {})


def test_add_wrong_details_type():
        with pytest.raises(TypeError):
            grocs.add_item('a new game', [])
