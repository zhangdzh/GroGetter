"""
This module is responsible for the users and their details
"""

TEST_USER_NAME = 'user2'
EMAIL = 'email'
USER_NAME = 'username'
REQUIRED_FIELDS = [EMAIL]

TEST_USER_NAME = 'user1'
TEST_EMAIL = 'user1@email.com'

users = {TEST_USER_NAME: {EMAIL: 'x@y.com'},
         'user2': {EMAIL: 'z@y.com'}}
# example structure of users list
# [
#     {
#         EMAIL: 'user1',
#         USER_NAME: 'user1'
#     },
#     {
#         EMAIL: 'user2',
#         USER_NAME: 'user2'
#     }
# ]


def user_exists(name):
    """
    Returns whether or not a user exists.
    """
    return name in users


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


def main():
    usernames = get_usernames()
    print(f'{usernames=}')


if __name__ == '__main__':
    main()
