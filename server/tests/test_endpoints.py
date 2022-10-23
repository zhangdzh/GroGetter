"""
Module for testing endpoints
"""
import server.endpoints as ep
import db.groc_types as gtyp
import db.users as usr

TEST_CLIENT = ep.app.test_client()
TEST_GROCERY_TYPES = gtyp.get_groc_types()


def test_get_grocery_type_list():
    """
    Check if grocery type list is proper
    """
    resp_json = TEST_CLIENT.get(ep.GROC_TYPE_LIST).get_json()
    assert isinstance(resp_json[ep.GROC_TYPE_LIST_NM], list)
    assert len(resp_json[ep.GROC_TYPE_LIST_NM]) > 0


def test_get_grocery_type_details():
    """
    Check if grocery type details are correct
    """
    for groc_type in TEST_GROCERY_TYPES:
        resp_json = TEST_CLIENT.get(
                f'{ep.GROC_TYPE_DETAILS}/{groc_type}').get_json()
        assert groc_type in resp_json
        assert isinstance(resp_json[groc_type], dict)


def test_add_grocery_list():
    """
    Check if grocery list can be added
    """
    pass


SAMPLE_USER_NM = 'SampleUser'
SAMPLE_USER = {
    usr.USER_NAME: SAMPLE_USER_NM,
    usr.EMAIL: 'x@y.com',
    usr.PASSWORD: 'xxx123'
}


def test_add_user():
    """
    Test adding a user.
    """
    resp = TEST_CLIENT.post(ep.USER_ADD, json=SAMPLE_USER)
    assert usr.user_exists(SAMPLE_USER_NM)
    usr.del_user(SAMPLE_USER_NM)
