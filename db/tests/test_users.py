"""
Testing module for users.py
"""

import pytest
import db.users as usr

TEST_USER_NAME = 'user1'
TEST_PW = "helloworld"
SAMPLE_PASSWORD = "password1234"

NEW_USER_NAME = 'user100'
NEW_DETAILS = {usr.EMAIL: 'new@email.com', usr.PASSWORD: 'swe'}


@pytest.fixture(scope='function')
def new_user():
    usr.add_user(NEW_USER_NAME, NEW_DETAILS)
    yield
    usr.del_user(NEW_USER_NAME)


def test_add_user():
    """
    tests add_user()
    """
    details = {}
    details[usr.USERNAME] = usr.TEST_USER_NAME
    details[usr.EMAIL] = usr.TEST_EMAIL
    details[usr.PASSWORD] = usr.TEST_PASSWORD
    usr.add_user(usr.TEST_USER_NAME, details)
    assert usr.user_exists(TEST_USER_NAME)
    usr.del_user(TEST_USER_NAME)


def test_add_wrong_name_type():
    with pytest.raises(TypeError):
        usr.add_user(7, {})


def test_add_wrong_details_type():
    with pytest.raises(TypeError):
        usr.add_user('a new user', [])


def test_add_missing_field():
    with pytest.raises(ValueError):
        usr.add_user('a new user', {'foo': 'bar'})


def test_get_usernames():
    """
    tests get_usernames()
    """
    usrs = usr.get_usernames()
    assert isinstance(usrs, list)
    # assert len(usrs) > 1


def test_get_users():
    usrs = usr.get_users()
    assert isinstance(usrs, list)
    # assert len(usrs) > 1


def test_get_user_email(new_user):
    """
    tests get_user_email()
    """
    email = usr.get_email(NEW_USER_NAME)
    assert isinstance(email, str)


def test_authenticate(new_user):
    """
    tests authenticate()
    """
    assert usr.authenticate(NEW_USER_NAME, NEW_DETAILS[usr.PASSWORD])


def test_change_password(new_user):
    """
    tests change_password()
    """
    test_pw = '99999'
    usr.change_password(NEW_USER_NAME, test_pw)
    assert usr.get_password(NEW_USER_NAME) == test_pw


def test_encrypted_password():
    """
    tests encrypt_password()
    """
    encrypted = usr.encrypt_password(SAMPLE_PASSWORD)
    assert SAMPLE_PASSWORD != encrypted


def test_wrong_password_type(new_user):
    with pytest.raises(TypeError):
        usr.change_password(NEW_USER_NAME, True)


def test_invalid_user_change_password():
    with pytest.raises(KeyError):
        usr.change_password("invalid", "123")
