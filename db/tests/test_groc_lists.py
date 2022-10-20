"""
Testing module for the groc_lists.py
"""
import pytest
import db.groc_lists as glst


TEST_DB = [
    {
        glst.USER_NAME: 'user1',
        glst.LIST_NAME: 'trip1',
        glst.NUM_ITEMS: 1,
        glst.GROC_LIST: {
            'itemA': '10-20-2022'
            }
    },
    {
        glst.USER_NAME: 'user2',
        glst.LIST_NAME: 'trip2',
        glst.NUM_ITEMS: 2,
        glst.GROC_LIST: {
            'itemB': '11-03-2022',
            'itemC': '10-30-2022'
        }
    }
]


def test_add_groc():
    glst.add_groc(TEST_DB[0][glst.USER_NAME], TEST_DB[0])
    glst.add_groc(TEST_DB[1][glst.USER_NAME], TEST_DB[1])
    assert glst.groc_lst_exists(TEST_DB[0][glst.USER_NAME])
    assert glst.groc_lst_exists(TEST_DB[1][glst.USER_NAME])


def test_add_wrong_username_type():
    with pytest.raises(TypeError):
        glst.add_groc(10, {})


def test_add_wrong_details_type():
    with pytest.raises(TypeError):
        glst.add_groc('new user list', [])


def test_add_missing_field():
    with pytest.raises(ValueError):
        glst.add_groc('new user list', {'foo': 'bar'})


def test_get_usernames():
    """
    tests get_usernames()
    """
    assert isinstance(glst.get_usernames(), list)


def test_get_details():
    """
    tests get_details()
    """
    assert isinstance(glst.get_details(TEST_DB[0][glst.USER_NAME]), dict)
    for field in glst.REQUIRED_FIELDS:
        assert field in glst.get_details(TEST_DB[0][glst.USER_NAME])


def test_get_user_groceries():
    assert isinstance(glst.get_user_groceries(TEST_DB[0][glst.USER_NAME]), dict)
    assert glst.get_user_groceries("FAKE USER") is None


def test_get_number_of_items():
    assert isinstance(glst.get_number_of_items(TEST_DB[0][glst.USER_NAME]), int)
    assert glst.get_number_of_items("FAKE USER") is None
