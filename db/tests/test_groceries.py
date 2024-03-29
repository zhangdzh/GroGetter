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


def test_get_items(new_groc_item):
    """
    tests get_items()
    """
    groceries = grocs.get_all_items()
    assert isinstance(groceries, list)
    assert len(groceries) > 0


def test_get_user_list():
    """
    tests get_user_list()
    """
    # completely new item
    temp = [
        {
            grocs.ITEM: "user_test",
            usr.USERNAME: "user_test",
            grocs.GROC_TYPE: grocs.CARBS,
            grocs.QUANTITY: 2,
            grocs.EXPIRATION_DATE: "10-31-2024"
        },
        {
            grocs.ITEM: "user_test2",
            usr.USERNAME: "user_test",
            grocs.GROC_TYPE: grocs.CARBS,
            grocs.QUANTITY: 2,
            grocs.EXPIRATION_DATE: "10-31-2024"
        }
    ]
    grocs.add_item(temp[0])
    grocs.add_item(temp[1])

    groceries = grocs.get_user_list(temp[0][usr.USERNAME])

    del temp[0]["_id"]
    del temp[1]["_id"]

    assert isinstance(groceries, list)
    assert len(groceries) > 0
    assert temp == groceries

    grocs.remove_item(temp[0][grocs.ITEM], temp[0][usr.USERNAME])
    grocs.remove_item(temp[1][grocs.ITEM], temp[1][usr.USERNAME])


def test_exists(new_groc_item):
    """
    tests exists()
    """
    assert grocs.exists(FIXTURE_GROC[grocs.ITEM], FIXTURE_GROC[usr.USERNAME])


def test_not_exists():
    """
    makes sure that exists works for non-existent items
    """
    assert not grocs.exists("definitely not a grocery item", "")


def test_get_details(new_groc_item):
    """
    tests get_details()
    """
    assert isinstance(grocs.get_details(
        FIXTURE_GROC[grocs.ITEM], FIXTURE_GROC[usr.USERNAME]), dict)
    for field in grocs.REQUIRED_FIELDS:
        assert field in grocs.get_details(
            FIXTURE_GROC[grocs.ITEM], FIXTURE_GROC[usr.USERNAME])
    with pytest.raises(KeyError):
        grocs.get_details("definitely not a grocery item", '')


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
    assert not grocs.exists(
        TEST_GROCERY[grocs.ITEM], TEST_GROCERY[usr.USERNAME])

    # test removing a non-existent item
    with pytest.raises(KeyError):
        grocs.remove_item("definitely not a grocery item", "")


def test_update_quanitity(new_groc_item):
    """
    tests update_item()
    """
    updated = {
        grocs.ITEM: "test",
        usr.USERNAME: usr.TEST_USER_NAME,
        grocs.GROC_TYPE: grocs.CARBS,
        grocs.QUANTITY: 4,
        grocs.EXPIRATION_DATE: "10-31-2024"
    }
    grocs.update_item(FIXTURE_GROC[grocs.ITEM],
                      FIXTURE_GROC[usr.USERNAME], updated)
    assert grocs.get_details(
        FIXTURE_GROC[grocs.ITEM], FIXTURE_GROC[usr.USERNAME]) == updated


def test_update_expiration_date(new_groc_item):
    """
    tests update_item()
    """
    updated = {
        grocs.ITEM: "test",
        usr.USERNAME: usr.TEST_USER_NAME,
        grocs.GROC_TYPE: grocs.CARBS,
        grocs.QUANTITY: 4,
        grocs.EXPIRATION_DATE: "10-31-2025"
    }

    grocs.update_item(FIXTURE_GROC[grocs.ITEM],
                      FIXTURE_GROC[usr.USERNAME], updated)
    assert grocs.get_details(
        FIXTURE_GROC[grocs.ITEM], FIXTURE_GROC[usr.USERNAME]) == updated


def test_update_groc_type(new_groc_item):
    """
    tests update_item()
    """
    updated = {
        grocs.ITEM: "test",
        usr.USERNAME: usr.TEST_USER_NAME,
        grocs.GROC_TYPE: grocs.MISC,
        grocs.QUANTITY: 4,
        grocs.EXPIRATION_DATE: "10-31-2025"
    }

    grocs.update_item(FIXTURE_GROC[grocs.ITEM],
                      FIXTURE_GROC[usr.USERNAME], updated)
    assert grocs.get_details(
        FIXTURE_GROC[grocs.ITEM], FIXTURE_GROC[usr.USERNAME]) == updated


def test_update_item_name_and_mult_field(new_groc_item):
    """
    tests update_item()
    """
    # change multiple fields
    updated = {
        grocs.ITEM: "test2",
        usr.USERNAME: usr.TEST_USER_NAME,
        grocs.GROC_TYPE: grocs.MISC,
        grocs.QUANTITY: 4,
        grocs.EXPIRATION_DATE: "10-31-2025"
    }

    grocs.update_item(FIXTURE_GROC[grocs.ITEM],
                      FIXTURE_GROC[usr.USERNAME], updated)
    assert grocs.get_details(
        updated[grocs.ITEM], updated[usr.USERNAME]) == updated

    # change back to original fixture
    updated = {
        grocs.ITEM: "test",
        usr.USERNAME: usr.TEST_USER_NAME,
        grocs.GROC_TYPE: grocs.CARBS,
        grocs.QUANTITY: 2,
        grocs.EXPIRATION_DATE: "10-31-2024"
    }

    grocs.update_item("test2", updated[usr.USERNAME], updated)
    assert grocs.get_details(
        updated[grocs.ITEM], updated[usr.USERNAME]) == updated


def test_get_types(new_groc_item):
    type_items = grocs.get_types(usr.TEST_USER_NAME)
    assert isinstance(type_items, list)
    assert len(type_items) > 0
