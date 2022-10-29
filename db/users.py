"""
This module is responsible for the users and their details
"""

TEST_USER_NAME = 'user2'
EMAIL = 'email'
PASSWORD = 'password'
USER_NAME = 'username'
REQUIRED_FIELDS = [EMAIL, PASSWORD]

TEST_USER_NAME = 'user1'
TEST_EMAIL = 'user1@email.com'
TEST_PASSWORD = 'xyz123'

users = {TEST_USER_NAME: {EMAIL: 'x@y.com', PASSWORD: 'xxx123'},
         'user2': {EMAIL: 'z@y.com', PASSWORD: 'yyy456'}}
# example structure of users list
# {
#     USER_NAME: {
#         EMAIL: 'user1'
#     },
#     'user2': {EMAIL: 'user2'}
# }


def user_exists(name):
    """
    Returns whether or not a user exists.
    """
    return name in users


def get_users_dict():
    return users


def get_usernames():
    """
    returns a list of usernames
    """
    return list(users.keys())


def del_user(name):
    del users[name]


def add_user(username, details):
    if not isinstance(username, str):
        raise TypeError(f'Wrong type for name: {type(username)=}')
    if not isinstance(details, dict):
        raise TypeError(f'Wrong type for details: {type(details)=}')
    print(details)
    for field in REQUIRED_FIELDS:
        if field not in details:
            raise ValueError(f'Required {field=} missing from details.')
    users[username] = details


def get_user_email(username):
    if not isinstance(username, str):
        raise TypeError(f'Wrong type for name: {type(username)=}')
    if username not in users.keys():
        raise KeyError('Username not found')
    return users[username].get(EMAIL)


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


def main():
    usernames = get_usernames()
    print(f'{usernames=}')


if __name__ == '__main__':
    main()
