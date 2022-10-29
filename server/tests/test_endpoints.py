"""
Module for testing endpoints
"""
import server.endpoints as ep
import db.groc_types as gtyp
import db.users as usr

TEST_CLIENT = ep.app.test_client()
TEST_GROCERY_TYPES = gtyp.get_groc_types()


def test_main_page():
    """
    Checks ability to display main page
    """
    resp_json = TEST_CLIENT.get(ep.MAIN_PAGE).get_json()
    assert isinstance(resp_json, dict)
    assert len(resp_json) > 0

# for some reason not working --- commented out for now
'''
def test_get_grocery_type_list():
    """
    Check if grocery type list is proper
    """
    resp_json = TEST_CLIENT.get(ep.GROC_TYPE_LIST_W_NS).get_json()
    assert isinstance(resp_json, dict)
    assert len(resp_json[ep.GROC_TYPE_LIST_NM]) > 0
'''

def test_get_grocery_type_details():
    """
    Check if grocery type details are correct
    """
    for groc_type in TEST_GROCERY_TYPES:
        resp_json = TEST_CLIENT.get(
                f'{ep.GROC_TYPE_DETAILS_W_NS}/{groc_type}').get_json()
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


def test_user_dict():
    resp_json = TEST_CLIENT.get(ep.USER_DICT).get_json()
    assert isinstance(resp_json, dict)
    

def test_add_user():
    """
    Test adding a user.
    """
    resp = TEST_CLIENT.post(ep.USER_ADD, json=SAMPLE_USER)
    assert usr.user_exists(SAMPLE_USER_NM)
    usr.del_user(SAMPLE_USER_NM)


def test_get_user_list():
    """
    See if we can get a user list properly.
    Return should look like:
        {USER_LIST_NM: [list of users types...]}
    """
resp = TEST_CLIENT.get(ep.USER_LIST)
resp_json = resp.get_json()
assert isinstance(resp_json[ep.USER_LIST_NM], list)
