"""
Module for testing endpoints
"""
from http import HTTPStatus
import server.endpoints as ep
import db.groc_types as gtyp
import db.users as usr
import db.groceries as groc
import pytest

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


def test_invalid_menu_option():
    resp_json = TEST_CLIENT.get(ep.MAIN_MENU).get_json()
    fake_option = 'bad'
    assert fake_option not in resp_json["Choices"].keys()


def test_get_grocery_type_list():
    """
    Check if grocery type list is proper
    """
    resp_json = TEST_CLIENT.get(f'/{ep.GROC_TYPES}/{ep.LIST}').get_json()
    print(resp_json)
    # resp_json[ep.GROC_TYPE_LIST_NM] --> keyerror with "grocery_types_list"
    assert isinstance(resp_json, dict)
    assert len(resp_json) > 0


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


def test_del_user():
    """
    Test deleting a user.
    """
    usr.add_user(SAMPLE_USER_NM, SAMPLE_USER)
    assert usr.user_exists(SAMPLE_USER_NM)
    print("after adding: ", usr.get_users_dict())
    resp = TEST_CLIENT.post(
        f'/{ep.USERS}/{ep.REMOVE}', json={usr.USER_NAME: SAMPLE_USER_NM})
    print("after removing: ", usr.get_users_dict())
    assert not usr.user_exists(SAMPLE_USER_NM)


def test_get_user_email():
    resp_json = TEST_CLIENT.get(
        f'/{ep.USERS}/{usr.EMAIL}/{usr.TEST_USER_NAME}').get_json()
    usr_email = resp_json[usr.EMAIL]
    assert usr_email == usr.TEST_EMAIL


# grocery endpoints tests
@pytest.mark.skip("Can't run this test until the we figure out MongoDB Connection.")
def test_get_groc_items():
    resp_json = TEST_CLIENT.get(f'/{ep.GROC}/{ep.ITEMS}').get_json()
    assert isinstance(resp_json, list)
    assert len(resp_json) > 0


def test_get_groc_items_not_found():
    resp = TEST_CLIENT.get(f'/{ep.GROC}/NotAnItem')
    assert resp.status_code == HTTPStatus.NOT_FOUND


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


@pytest.mark.skip("Can't run this test until the we figure out MongoDB Connection.")
def test_add_and_remove_grocitem():
    resp_json = TEST_CLIENT.post(f'/{ep.GROC}/{ep.ADD}', json=SAMPLE_GROCLIST)
    assert groc.exists(SAMPLE_GROCITEM_NM)
    resp_json = TEST_CLIENT.post(
        f'/{ep.GROC}/{ep.REMOVE}', json=SAMPLE_REMOVE_GROCITEM_NM)
    assert not groc.exists(SAMPLE_GROCITEM_NM)


@pytest.mark.skip("Can't run this test until the we figure out MongoDB Connection.")
def test_get_groc_details():
    resp_json = TEST_CLIENT.get(f'/{ep.GROC}/{ep.DETAILS}/item1').get_json()
    assert isinstance(resp_json, dict)
    for field in groc.REQUIRED_FIELDS:
        assert field in resp_json


@pytest.mark.skip("Can't run this test until the we figure out MongoDB Connection.")
def test_update_grocitem():
    groc.add_item(SAMPLE_GROCITEM_NM, SAMPLE_GROCLIST)
    assert groc.exists(SAMPLE_GROCITEM_NM)
    SAMPLE_GROCLIST[groc.QUANTITY] = 20
    SAMPLE_GROCLIST[groc.EXPIRATION_DATE] = "10/30/2022"
    resp_json = TEST_CLIENT.post(
        f'/{ep.GROC}/{ep.UPDATE}', json=SAMPLE_GROCLIST)
    assert groc.exists(SAMPLE_GROCITEM_NM)
    assert groc.get_details(SAMPLE_GROCITEM_NM)[groc.QUANTITY] == 20
    assert groc.get_details(SAMPLE_GROCITEM_NM)[
        groc.EXPIRATION_DATE] == "10/30/2022"
    groc.remove_item(SAMPLE_GROCITEM_NM)


def test_update_groc_type():
    groc.add_item(SAMPLE_GROCITEM_NM, SAMPLE_GROCLIST)
    assert groc.exists(SAMPLE_GROCITEM_NM)
    SAMPLE_GROCLIST[groc.GROC_TYPE] = 'Fruit'
    resp_json = TEST_CLIENT.post(
        f'/{ep.GROC}/{ep.UPDATE}_{ep.GROC_TYPES}', json=SAMPLE_GROCLIST)
    assert groc.exists(SAMPLE_GROCITEM_NM)
    assert groc.get_details(SAMPLE_GROCITEM_NM)[groc.GROC_TYPE] == 'Fruit'
    groc.remove_item(SAMPLE_GROCITEM_NM)


def test_update_quantity():
    groc.add_item(SAMPLE_GROCITEM_NM, SAMPLE_GROCLIST)
    assert groc.exists(SAMPLE_GROCITEM_NM)
    SAMPLE_GROCLIST[groc.QUANTITY] = 15
    resp_json = TEST_CLIENT.post(
        f'/{ep.GROC}/{ep.UPDATE}_{ep.QUANTITY}', json=SAMPLE_GROCLIST)
    assert groc.exists(SAMPLE_GROCITEM_NM)
    assert groc.get_details(SAMPLE_GROCITEM_NM)[groc.QUANTITY] == 15
    groc.remove_item(SAMPLE_GROCITEM_NM)


def test_update_expiration():  # Temporary so we remember to fill this in
    pass
