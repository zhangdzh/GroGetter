
import pytest

import server.endpoints as ep
import db.grocery_types

TEST_CLIENT = ep.app.test_client()
TEST_GROC_TYPE = 'Meat'
TEST_GROCERY_TYPTES = db.grocery_types.get_groc_types()


# def test_hello():
#     assert True


def test_get_grocery_type_list():
    """
    Check if grocery type list is proper
    """
    resp_json = TEST_CLIENT.get(ep.GROC_TYPE_LIST).get_json()
    assert isinstance(resp_json[ep.GROC_TYPE_LIST_NM], list)


def test_get_grocery_type_list_not_empty():
    """
    Check if grocery type list is not empty
    """
    resp_json = TEST_CLIENT.get(ep.GROC_TYPE_LIST).get_json()
    assert len(resp_json[ep.GROC_TYPE_LIST_NM]) > 0
    


def test_get_grocery_type_details():
    """
    Check if grocery type details are correct
    """
    for groc_type in TEST_GROCERY_TYPTES:
        resp_json = TEST_CLIENT.get(f'{ep.GROC_TYPE_DETAILS}/{groc_type}').get_json()
        assert groc_type in resp_json
        assert isinstance(resp_json[groc_type], dict)
