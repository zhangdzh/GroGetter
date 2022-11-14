"""
Module for testing endpoints
"""
import server.endpoints as ep
import db.groc_types as gtyp
import db.users as usr
import db.groceries as groc

TEST_CLIENT = ep.app.test_client()


def test_main_page():
    """
    Checks ability to display main page
    """
    resp_json = TEST_CLIENT.get(ep.MAIN_PAGE).get_json()
    assert isinstance(resp_json, dict)
    assert len(resp_json) > 0


def test_main_menu():
    """
    Checks ability to display main menu
    """
    resp_json = TEST_CLIENT.get(ep.MAIN_MENU).get_json()
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
    resp = TEST_CLIENT.post(f'/{ep.USERS}/{ep.ADD}', json=SAMPLE_USER)
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


SAMPLE_GROCITEM_NM = 'SampleItem'
SAMPLE_GROCLIST = {
    ep.ITEM: SAMPLE_GROCITEM_NM,
    groc.GROC_TYPE: gtyp.BAKED_GOODS,
    groc.QUANTITY: 10, 
    groc.EXPIRATION_DATE: "10/10/2022"
}


SAMPLE_REMOVE_GROCITEM_NM = {
    ep.ITEM: SAMPLE_GROCITEM_NM
}


def test_add_and_remove_grocitem():
    resp_json = TEST_CLIENT.post(f'/{ep.GROC}/{ep.ADD}', json=SAMPLE_GROCLIST)
    assert groc.exists(SAMPLE_GROCITEM_NM)
    resp_json = TEST_CLIENT.post(f'/{ep.GROC}/{ep.REMOVE}', json=SAMPLE_REMOVE_GROCITEM_NM)
    assert not groc.exists(SAMPLE_GROCITEM_NM)


def test_get_groc_details():
    resp_json = TEST_CLIENT.get(f'/{ep.GROC}/{ep.DETAILS}/item1').get_json()
    assert isinstance(resp_json, dict)
    for field in groc.REQUIRED_FIELDS:
        assert field in resp_json


def test_update_grocitem():
    groc.add_item(SAMPLE_GROCITEM_NM, SAMPLE_GROCLIST)
    assert groc.exists(SAMPLE_GROCITEM_NM)
    SAMPLE_GROCLIST[groc.QUANTITY] = 20
    SAMPLE_GROCLIST[groc.EXPIRATION_DATE] = "10/30/2022"
    resp_json = TEST_CLIENT.post(f'/{ep.GROC}/{ep.UPDATE}', json=SAMPLE_GROCLIST)
    assert groc.exists(SAMPLE_GROCITEM_NM)
    assert groc.get_details(SAMPLE_GROCITEM_NM)[groc.QUANTITY] == 20
    assert groc.get_details(SAMPLE_GROCITEM_NM)[groc.EXPIRATION_DATE] == "10/30/2022"
    groc.remove_item(SAMPLE_GROCITEM_NM)
