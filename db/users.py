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


# TODO: change all functions to use db


def user_exists(name):
    """
    Returns whether or not a user exists.
    """
    pass


# Mongo
def get_users() -> list:
    """
    Returns a list of the users
    """
    dbc.connect_db()
    return dbc.fetch_all(USER_COLLECT)


# Mongo
def get_usernames():
    """
    returns a list of usernames
    """
    dbc.connect_db()
    all = dbc.fetch_all(USER_COLLECT)
    users = []
    for user in all:
        users.append(user[USERNAME])
    return users


# Mongo
def del_user(name):
    dbc.connect_db()
    filter = {USERNAME: name}
    dbc.del_one(USER_COLLECT, filter)


# Mongo
def add_user(username, details):
    """
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
    dbc.insert_one(USER_COLLECT, doc)


# Mongo
def get_email(username):
    if not isinstance(username, str):
        raise TypeError(f'Wrong type for name: {type(username)=}')
    dbc.connect_db()
    filter = {USERNAME: username}
    return dbc.fetch_one(USER_COLLECT, filter)[EMAIL]


def get_user_password(username):
    if not isinstance(username, str):
        raise TypeError(f'Wrong type for name: {type(username)=}')
    if username not in users.keys():
        raise KeyError('Username not found')
    return users[username].get(PASSWORD)


def change_password(username, new_password):
    """
    Changes user's password.
    Note: In implementation, should precede this method call
    by ensuring that the same password is entered twice.
    """
    if not isinstance(new_password, str):
        raise TypeError
    if username not in users.keys():
        raise KeyError("Username not found")
    users[username][PASSWORD] = new_password


def encrypt_password(password):
    encrypted = hashlib.sha1(password.encode('utf-8')).hexdigest().strip()
    return encrypted


def main():
    usernames = get_usernames()
    print(f'{usernames=}')


if __name__ == '__main__':
    main()
