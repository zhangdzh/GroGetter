"""
Testing module for the groceries.py
"""
import pytest
import os
import db.groceries as grocs
import db.users as usr


FIXTURE_GROC = {
    grocs.ITEM: "test",
    usr.USERNAME: usr.TEST_USER_NAME,
    grocs.GROC_TYPE: grocs.CARBS,
    grocs.QUANTITY: 2,
    grocs.EXPIRATION_DATE: "10-31-2024"
}

RUNNING_ON_CICD_SERVER = os.environ.get('CI', False)

TEST_DEL_GROC = "Grocery to be deleted"

# All need to be checked and fixed!!


@pytest.fixture(scope='function')
def new_groc_item():
    grocs.add_item(FIXTURE_GROC)
    yield
    grocs.remove_item(FIXTURE_GROC[grocs.ITEM], FIXTURE_GROC[usr.USERNAME])


# @pytest.fixture(scope='function')
# def test_del_groc(new_groc):
#     grocs.del_groc(TEST_DEL_GROC)
#     assert not grocs.exists(TEST_DEL_GROC)


def test_get_items():
    """
    tests get_items()
    """
    groceries = grocs.get_all_items()
    assert isinstance(groceries, list)
    assert len(groceries) > 0


def test_get_user_list(new_groc_item):
    """
    tests get_user_list()
    """
    groceries = grocs.get_user_list(FIXTURE_GROC[usr.USERNAME])
    assert isinstance(groceries, list)
    assert len(groceries) > 0
    assert FIXTURE_GROC == groceries[0]

# @pytest.mark.skip("Can't run this test until the we figure out MongoDB Connection.")
# # gives pymongo.errors.ServerSelectionTimeoutError
# def test_get_grocery_list():
#     """
#     tests get_grocery_list()
#     """
#     '''
#     groc_list = grocs.get_grocery_list()
#     assert isinstance(groc_list, dict)
#     assert len(groc_list) > 0
#     for item in groc_list:
#         assert isinstance(item, str)
#         assert isinstance(groc_list[item], dict)
#     '''
#     if not RUNNING_ON_CICD_SERVER:
#         groceries = grocs.get_grocery_list(usr.TEST_USER_NAME)
#         assert isinstance(groceries, list)
#         # length later - perhaps after adding fixture to create new
#         # note: dict currently empty?


# @pytest.mark.skip("Can't run this test until the we figure out MongoDB Connection.")
def test_exists(new_groc_item):
    """
    tests exists()
    """
    assert grocs.exists(FIXTURE_GROC[grocs.ITEM], FIXTURE_GROC[usr.USERNAME])


# @pytest.mark.skip("Can't run this test until the we figure out MongoDB Connection.")
def test_not_exists():
    """
    makes sure that exists works for non-existent items
    """
    assert not grocs.exists("definitely not a grocery item", "")


@pytest.mark.skip("Can't run this test until the we figure out MongoDB Connection.")
def test_get_details(new_groc_item):
    """
    tests get_details()
    """
    assert isinstance(grocs.get_details(FIXTURE_GROC[usr.USERNAME]), dict)
    for field in grocs.REQUIRED_FIELDS:
        assert field in grocs.get_details(FIXTURE_GROC[usr.USERNAME])
    with pytest.raises(KeyError):
        grocs.get_details("definitely not a grocery item")


@pytest.mark.skip("Can't run this test until the we figure out MongoDB Connection.")
def test_add_and_remove_item():
    """
    tests add_item() and remove_item()
    """
    TEST_GROCERY = {
        grocs.ITEM: "item2",
        usr.USERNAME: "user1",
        grocs.GROC_TYPE: grocs.MISC,
        grocs.QUANTITY: 10,
        grocs.EXPIRATION_DATE: "10-20-2022"
    }
    # add the item
    grocs.add_item(TEST_GROCERY)
    assert grocs.exists(TEST_GROCERY[grocs.ITEM], TEST_GROCERY[usr.USERNAME])

    # remove the item
    grocs.remove_item(TEST_GROCERY[grocs.ITEM], TEST_GROCERY[usr.USERNAME])
    assert not grocs.exists(TEST_GROCERY[grocs.ITEM], TEST_GROCERY[usr.USERNAME])

    # test removing a non-existent item
    with pytest.raises(KeyError):
        grocs.remove_item("definitely not a grocery item", "")


@pytest.mark.skip("Can't run this test until the we figure out MongoDB Connection.")
def test_update_item(new_groc_item):
    """
    tests update_item()
    """
    # TEST_ITEM = "item1"
    TEST_GROCERY = {
        grocs.GROC_TYPE: grocs.MISC,
        grocs.QUANTITY: 10,
        grocs.EXPIRATION_DATE: "10-20-2022"
    }
    grocs.update_item(FIXTURE_GROC[usr.USERNAME], TEST_GROCERY)
    assert TEST_GROCERY == grocs.get_details(FIXTURE_GROC[usr.USERNAME])


@pytest.mark.skip("Can't run this test until the we figure out MongoDB Connection.")
def test_raised_exceptions_for_add_item():
    """
    tests raised exceptions for add_item()
    """
    TEST_GROCERY = {

        grocs.GROC_TYPE: grocs.MISC,
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


@pytest.mark.skip("Can't run this test until the we figure out MongoDB Connection.")
def test_update_quantity(new_groc_item):
    """
    tests update_quantity()
    """
    # TEST_ITEM = "item1"
    TEST_GROC_TYPE = 'Fruit'
    grocs.update_groc_type(FIXTURE_GROC[usr.USERNAME], TEST_GROC_TYPE)
    assert TEST_GROC_TYPE == grocs.get_details(FIXTURE_GROC[usr.USERNAME])[grocs.GROC_TYPE]


@pytest.mark.skip("Can't run this test until the we figure out MongoDB Connection.")
def test_update_quantity(new_groc_item):
    """
    tests update_quantity()
    """
    # TEST_ITEM = "item1"
    TEST_QUANTITY = 20
    grocs.update_quantity(FIXTURE_GROC[usr.USERNAME], TEST_QUANTITY)
    assert TEST_QUANTITY == grocs.get_details(FIXTURE_GROC[usr.USERNAME])[grocs.QUANTITY]


@pytest.mark.skip("Can't run this test until the we figure out MongoDB Connection.")
def test_update_expiration(new_groc_item):
    """
    tests update_expiration()
    """
    TEST_EXP = "10-02-2022"
    grocs.update_quantity(FIXTURE_GROC[usr.USERNAME], TEST_EXP)
    assert TEST_EXP == grocs.get_details(FIXTURE_GROC[usr.USERNAME])[grocs.EXPIRATION_DATE]


@pytest.mark.skip("Can't run this test until the we figure out MongoDB Connection.")
def test_add_item_dup(new_groc_item):
    with pytest.raises(ValueError):
        grocs.add_item(FIXTURE_GROC[usr.USERNAME], FIXTURE_GROC)


@pytest.mark.skip("Can't run this test until the we figure out MongoDB Connection.")
def test_add_wrong_name_type():
    with pytest.raises(TypeError):
        grocs.add_item(7, {})


@pytest.mark.skip("Can't run this test until the we figure out MongoDB Connection.")
def test_add_wrong_details_type():
    with pytest.raises(TypeError):
        grocs.add_item('a new game', [])


@pytest.mark.skip("Can't run this test until the we figure out MongoDB Connection.")
def test_add_missing_field():
    with pytest.raises(KeyError):
        grocs.add_item('a new game', {'foo': 'bar'})


@pytest.mark.skip("Can't run this test until the we figure out MongoDB Connection.")
def test_get_grocs_by_type(new_groc_item):
    type_items = grocs.get_grocs_by_type(grocs.CARBS)
    assert isinstance(type_items, dict)
    assert len(type_items) > 0
