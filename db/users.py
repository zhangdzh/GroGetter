"""
This module is responsible for the users and their details
"""

EMAIL = 'email'
USER_NAME = 'username'
REQUIRED_FIELDS = [EMAIL, USER_NAME]

TEST_USER_NAME = 'user1'
TEST_EMAIL = 'user1@email.com'


users = [
    {
        EMAIL: TEST_EMAIL,
        USER_NAME: TEST_USER_NAME
    }
]
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
