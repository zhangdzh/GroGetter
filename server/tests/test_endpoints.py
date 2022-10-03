
import pytest

import server.endpoints as ep

TEST_CLIENT = ep.app.test_client()
TEST_GROC_TYPE = 'Meat'


def test_hello():
    assert True


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
    

def test_get_grocery_type_detail():
    """
    Check if grocery detail is returned
    """
    resp_json = TEST_CLIENT.get(f'{ep.GROC_TYPE_DETAILS}/{TEST_GROC_TYPE}').get_json()
    assert TEST_GROC_TYPE in resp_json
    assert isinstance(resp_json[TEST_GROC_TYPE], dict)

