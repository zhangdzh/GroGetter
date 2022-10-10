'''
This module encapsulates details about a user's grocery list
'''

TEST_USER_NAME = 'user1'
USER_NAME = 'name'
LIST_NAME = 'list_name'
NUM_ITEMS = 'num_items'
GROC_LISTS = 'groc_lists'

REQUIRED_FIELDS = [USER_NAME, LIST_NAME, NUM_ITEMS, GROC_LISTS]
# lists = {
#     USER_NAME: {
#         LIST_NAME: 'trip1',
#         NUM_ITEMS: 1,
#         GROC_LISTS: {
#             'itemA': '10-20-2022'
#         }
#     },
#     'user2': {
#         LIST_NAME: 'trip2',
#         NUM_ITEMS: 2,
#         GROC_LISTS: {
#             'itemB': '11-03-2022',
#             'itemC': '10-30-2022'
#         }
#     }
# }


lists = [
    {
        USER_NAME: 'user1',
        LIST_NAME: 'trip1',
        NUM_ITEMS: 1,
        GROC_LISTS: {
            'itemA': '10-20-2022'
        }
    },
    {
        USER_NAME: 'user2',
        LIST_NAME: 'trip2',
        NUM_ITEMS: 2,
        GROC_LISTS: {
            'itemB': '11-03-2022',
            'itemC': '10-30-2022'
        }
    }
]


def groc_lst_exists(username):
    """
    returns groc_list for specific user
    """
    for groc in lists:
        if groc[USER_NAME] == username:
            return groc


def get_usernames():
    """
    returns a list of usernames
    """
    return [user[USER_NAME] for user in lists]


def get_details(username):
    """
    returns a dictionary of details for a user
    """
    for user in lists:
        if user[USER_NAME] == username:
            return user


def add_groc(username, details):
    """
    add new groc_list to database
    """
    if not isinstance(username, str):
        raise TypeError(f'Wrong type for name: {type(username)=}')
    if not isinstance(details, dict):
        raise TypeError(f'Wrong type for details: {type(details)=}')
    for field in REQUIRED_FIELDS:
        if field not in details:
            raise ValueError(f'Required {field=} missing from details.')
    lists[len(lists)-1] = details


def main():
    usernames = get_usernames()
    print(usernames)


if __name__ == '__main__':
    main()
