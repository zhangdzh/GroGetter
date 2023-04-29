"""
Module for testing endpoints
"""
from http import HTTPStatus
import server.endpoints as ep
import db.users as usr
import db.groceries as grocs
import pytest

TEST_CLIENT = ep.app.test_client()
TEST_E_ITEM = 'test_endpts_item'
TEST_USER = 'test_endpts_user'
TEST_DETAILS = {usr.EMAIL: 'new@email.com', usr.PASSWORD: 'swe'}


@pytest.fixture(scope='function')
def new_user_with_item():
    usr.add_user(TEST_USER, TEST_DETAILS)

    item = {
        usr.USERNAME: TEST_USER,
        grocs.ITEM: TEST_E_ITEM,
        grocs.GROC_TYPE: grocs.CARBS,
        grocs.QUANTITY: 99,
        grocs.EXPIRATION_DATE: '05-08-2023'
    }

    grocs.add_item(item)

    yield

    grocs.remove_item(TEST_E_ITEM, TEST_USER)
    usr.del_user(TEST_USER)


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


def test_n_records():
    resp_json = TEST_CLIENT.get(f'/{ep.DEVELOPER}/n_{ep.RECORDS}').get_json()
    assert isinstance(resp_json, int)


def test_get_groc_type_list(new_user_with_item):
    """
    Check if grocery type list is proper
    """
    resp_json = TEST_CLIENT.get(
        f'/{ep.GROC}/{ep.GROC}_{ep.TYPES}_{ep.LIST}/{TEST_USER}').get_json()
    print(resp_json)
    # resp_json[ep.GROC_TYPE_LIST_NM] --> keyerror with "grocery_types_list"
    assert isinstance(resp_json, list)
    assert len(resp_json) > 0


SAMPLE_USER = {
    usr.USERNAME: TEST_USER,
    usr.EMAIL: TEST_DETAILS[usr.EMAIL],
    usr.PASSWORD: TEST_DETAILS[usr.PASSWORD]
}


def test_add_user():
    """
    Test adding a user.
    """
    resp = TEST_CLIENT.post(f'/{ep.USERS}/{ep.ADD}', json=SAMPLE_USER)
    assert usr.user_exists(TEST_USER)
    usr.del_user(TEST_USER)


def test_get_user_list(new_user_with_item):
    """
    Check if we can get a list of usernames
    """
    resp_json = TEST_CLIENT.get(f'/{ep.USERS}/{ep.LIST}').get_json()
    assert isinstance(resp_json, list)
    assert TEST_USER in resp_json


def test_del_user():
    """
    Test deleting a user.
    """
    usr.add_user(TEST_USER, TEST_DETAILS)
    assert usr.user_exists(TEST_USER)
    resp = TEST_CLIENT.post(
        f'/{ep.USERS}/{ep.REMOVE}', json={usr.USERNAME: TEST_USER})
    assert not usr.user_exists(TEST_USER)


def test_get_user_email(new_user_with_item):
    resp_json = TEST_CLIENT.get(
        f'/{ep.USERS}/{usr.EMAIL}/{TEST_USER}').get_json()
    assert str(resp_json) == TEST_DETAILS[usr.EMAIL]


def test_login():
    """
    Test login endpoint
    """
    resp = TEST_CLIENT.post(
        f'/{ep.USERS}/{ep.LOGIN}', json={usr.USERNAME: usr.TEST_USER_NAME, usr.PASSWORD: usr.TEST_PASSWORD})
    assert resp.status_code == HTTPStatus.OK


# grocery endpoints tests
def test_get_groc_items(new_user_with_item):
    resp_json = TEST_CLIENT.get(
        f'/{ep.GROC}/{ep.ITEMS}/{TEST_USER}').get_json()
    assert isinstance(resp_json, list)
    assert len(resp_json) > 0


def test_get_groc_items_not_found():
    resp = TEST_CLIENT.get(f'/{ep.GROC}/NotAnItem')
    assert resp.status_code == HTTPStatus.NOT_FOUND


SAMPLE_GROCITEM_NM = 'SampleItem'
SAMPLE_GROCLIST = {
    usr.USERNAME: TEST_USER,
    grocs.ITEM: SAMPLE_GROCITEM_NM,
    grocs.GROC_TYPE: grocs.BAKED_GOODS,
    grocs.QUANTITY: 10,
    grocs.EXPIRATION_DATE: "10-10-2022"
}


SAMPLE_REMOVE_GROCITEM_NM = {
    grocs.ITEM: SAMPLE_GROCITEM_NM,
    usr.USERNAME: TEST_USER
}


def test_add_and_remove_item():
    resp_json = TEST_CLIENT.post(f'/{ep.GROC}/{ep.ADD}', json=SAMPLE_GROCLIST)
    assert grocs.exists(SAMPLE_GROCITEM_NM, TEST_USER)
    resp_json = TEST_CLIENT.delete(
        f'/{ep.GROC}/{ep.REMOVE}', json=SAMPLE_REMOVE_GROCITEM_NM)
    # grocs.remove_item(SAMPLE_GROCITEM_NM, TEST_USER)
    assert not grocs.exists(SAMPLE_GROCITEM_NM, TEST_USER)


@pytest.mark.skip("Can't run this test until the we figure out MongoDB Connection.")
def test_get_groc_details():
    resp_json = TEST_CLIENT.get(f'/{ep.GROC}/{ep.DETAILS}/item1').get_json()
    assert isinstance(resp_json, dict)
    for field in grocs.REQUIRED_FIELDS:
        assert field in resp_json


@pytest.mark.skip("Can't run this test until the we figure out MongoDB Connection.")
def test_update_groc_item():
    # note: currently only testing that quantity is updated
    grocs.add_item(SAMPLE_GROCITEM_NM, SAMPLE_GROCLIST)
    assert grocs.exists(SAMPLE_GROCITEM_NM)
    SAMPLE_GROCLIST[grocs.QUANTITY] = 20
    SAMPLE_GROCLIST[grocs.EXPIRATION_DATE] = "10/30/2022"
    resp_json = TEST_CLIENT.put(
        f'/{ep.GROC}/{ep.UPDATE}/{ep.QUANTITY}/100', json={groc.ITEM: SAMPLE_GROCITEM_NM})
    assert grocs.exists(SAMPLE_GROCITEM_NM)
    assert grocs.get_details(SAMPLE_GROCITEM_NM)[grocs.QUANTITY] == 100
    # assert grocs.get_details(SAMPLE_GROCITEM_NM)[
    #     grocs.EXPIRATION_DATE] == "10/30/2022"
    grocs.remove_item(SAMPLE_GROCITEM_NM)
