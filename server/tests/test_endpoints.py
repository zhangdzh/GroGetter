
import pytest

import server.endpoints as ep

TEST_CLIENT = ep.app.test_client()


def test_hello():
    assert True


def test_get_grocery_type_list():
    """
    Check if grocery type list is proper
    """
    resp_json = TEST_CLIENT.get(ep.GROCERY_TYPE_LIST).get_json()
    assert isinstance(resp_json[ep.GROCERY_TYPE_LIST_NM], list)