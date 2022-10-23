"""
This module is responsible for the users and their details
"""

EMAIL = 'email'
USER_NAME = 'username'
REQUIRED_FIELDS = [EMAIL, USER_NAME]

TEST_USER_NAME = 'user1'
TEST_EMAIL = 'user1@email.com'


users = []
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


def get_usernames():
    """
    returns a list of usernames
    """
    return [user[USER_NAME] for user in users]


def del_user(name):
    del users[name]


def add_user(username, details):
    """
    adds a user to the list of users
    """
    if not isinstance(username, str):
        raise TypeError('username must be a string')
    if not isinstance(details, dict):
        raise TypeError('details must be a dictionary')
    for field in REQUIRED_FIELDS:
        if field not in details:
            raise ValueError('details must contain {}'.format(field))
    users.append(details)


def main():
    usernames = get_usernames()
    print(f'{usernames=}')


if __name__ == '__main__':
    main()
