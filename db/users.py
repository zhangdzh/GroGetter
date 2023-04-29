"""
This module is responsible for the users and their details
"""
import hashlib
import db.db_connect as dbc

# TEST_USER_NAME = 'user2'
EMAIL = 'email'
PASSWORD = 'password'
USERNAME = 'username'
REQUIRED_FIELDS = [EMAIL, PASSWORD]

TEST_USER_NAME = 'user1'
TEST_EMAIL = 'user1@email.com'
TEST_PASSWORD = 'xyz123'

# Mongo
USER_COLLECT = 'userdb'

# users = {TEST_USER_NAME: {
#     EMAIL: TEST_EMAIL, PASSWORD: TEST_PASSWORD},
#     'user2': {
#     EMAIL: 'z@y.com', PASSWORD: 'yyy456'}}

# sample document
'''
{
    username: 'user1',
    email: 'user1@email.com',
    password: 'abc123'
}
'''


def user_exists(name):
    """
    Returns whether or not a user exists.
    :param name: Username
    """
    if name in get_usernames():
        return True
    else:
        return False


def get_users() -> list:
    """
    Returns a list of the users
    """
    dbc.connect_db()
    return dbc.fetch_all(USER_COLLECT)


def get_usernames() -> list:
    """
    Returns a list of usernames
    """
    dbc.connect_db()
    all = dbc.fetch_all(USER_COLLECT)
    users = []
    for user in all:
        users.append(user[USERNAME])
    return users


def del_user(name):
    """
    Deletes a user from collection
    :param name: User name
    """
    dbc.connect_db()
    filter = {USERNAME: name}
    dbc.del_one(USER_COLLECT, filter)


def add_user(username, details):
    """
    Adds user to collection
    :param username: string
    :param details: Dictionary with keys email and password
    """
    if not isinstance(username, str):
        raise TypeError(f'Wrong type for name: {type(username)=}')
    if not isinstance(details, dict):
        raise TypeError(f'Wrong type for details: {type(details)=}')
    for field in REQUIRED_FIELDS:
        if field not in details:
            raise ValueError(f'Required {field=} missing from details.')
    doc = details
    doc[USERNAME] = username
    dbc.connect_db()

    # note: should encrypt password here before inserting

    dbc.insert_one(USER_COLLECT, doc)


def get_email(username):
    """
    Gets user's name
    :param username: User name
    """
    if not isinstance(username, str):
        raise TypeError(f'Wrong type for name: {type(username)=}')
    dbc.connect_db()
    filter = {USERNAME: username}
    return dbc.fetch_one(USER_COLLECT, filter)[EMAIL]


def get_password(username):
    """
    Gets user's password
    :param username: User name
    """
    if not isinstance(username, str):
        raise TypeError(f'Wrong type for name: {type(username)=}')
    dbc.connect_db()
    filter = {USERNAME: username}
    return dbc.fetch_one(USER_COLLECT, filter)[PASSWORD]


def authenticate(username, password):
    """
    Returns whether or not the username and password match.
    :param username: User name
    :param password: Password to authenticate
    """
    if not isinstance(username, str):
        raise TypeError(f'Wrong type for name: {type(username)=}')
    if not isinstance(password, str):
        raise TypeError(f'Wrong type for password: {type(password)=}')
    dbc.connect_db()
    filter = {USERNAME: username}
    user = dbc.fetch_one(USER_COLLECT, filter)
    if user is None:
        return False
    # TODO: encrypted version of password
    # if encrypt_password(password) == user[PASSWORD]:
    if password == user[PASSWORD]:
        return True
    else:
        return False


def change_password(username, new_password):
    """
    Changes user's password.
    Note: In implementation, should precede this method call
    by ensuring that the same password is entered twice.
    :param username: User name
    :param new_password: New password
    """
    if not isinstance(new_password, str):
        raise TypeError
    if username not in get_usernames():
        raise KeyError("Username not found")
    filter = {USERNAME: username}
    dbc.connect_db()
    new = {PASSWORD: new_password}
    return dbc.update_one(USER_COLLECT, filter, new)


def encrypt_password(password):
    """
    Returns encrypted password
    :param password: Unencrypted password
    """
    encrypted = hashlib.sha1(password.encode('utf-8')).hexdigest().strip()
    return encrypted


def purge():
    """
    Deletes all items from collection
    """
    dbc.connect_db()
    dbc.delete_many(USER_COLLECT, {})


def main():
    usernames = get_usernames()
    print(f'{usernames=}')


if __name__ == '__main__':
    main()
