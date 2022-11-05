"""
Module for testing endpoints
"""
import server.endpoints as ep
import db.groc_types as gtyp
import db.users as usr

TEST_CLIENT = ep.app.test_client()


def test_main_page():
    """
    Checks ability to display main page
    """
    resp_json = TEST_CLIENT.get(ep.MAIN_PAGE).get_json()
    assert isinstance(resp_json, dict)
    assert len(resp_json) > 0


def test_get_grocery_type_list():
    """
    Check if grocery type list is proper
    """
    resp_json = TEST_CLIENT.get(f'/{ep.GROC_TYPES}/{ep.LIST}').get_json()
    print(resp_json)
    # resp_json[ep.GROC_TYPE_LIST_NM] --> keyerror with "grocery_types_list"
    assert isinstance(resp_json, dict)
    assert len(resp_json) > 0

def test_get_grocery_type_details():
    """
    Check if grocery type details are correct
    """
    # for groc_type in gtyp.get_groc_types():
    #     resp_json = TEST_CLIENT.get(
    #             f'{ep.GROC_TYPE_DETAILS_W_NS}/{groc_type}').get_json()
    #     assert groc_type in resp_json
    #     assert isinstance(resp_json[groc_type], dict)



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
    resp_json = TEST_CLIENT.get(f'/{ep.USERS}/{ep.DICT}').get_json()
    assert isinstance(resp_json, dict)
    assert len(resp_json) > 1 
    

def test_add_user():
    """
    Test adding a user.
    """
    print(dir(TEST_CLIENT))
    resp = TEST_CLIENT.post(f'/{ep.USERS}/{ep.ADD}', json=SAMPLE_USER)
    print(resp)
    assert usr.user_exists(SAMPLE_USER_NM)
    usr.del_user(SAMPLE_USER_NM)


def test_get_user_list():
    """
    See if we can get a user list properly.
    Return should look like:
        {USER_LIST_NM: [list of users types...]}
    """
    resp_json = TEST_CLIENT.get(f'/{ep.USERS}/{ep.LIST}').get_json()
    assert isinstance(resp_json, dict)
    assert isinstance(resp_json[ep.USER_LIST_NM], list)


# grocery endpoints tests
def test_get_groc_items():
    resp_json = TEST_CLIENT.get(f'/{ep.GROC}/{ep.ITEMS}').get_json()
    assert isinstance(resp_json, list)
    assert len(resp_json) > 0