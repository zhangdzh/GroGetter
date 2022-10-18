'''
This module encapsulates details about a user's grocery list
'''

TEST_USER_NAME = 'user1'
USER_NAME = 'name'
LIST_NAME = 'list_name'
NUM_ITEMS = 'num_items'
GROC_LIST = 'groc_list'

REQUIRED_FIELDS = [USER_NAME, LIST_NAME, NUM_ITEMS, GROC_LIST]

lists = []
# example of what list should look like
# {
#     USER_NAME: 'user1',
#     LIST_NAME: 'trip1',
#     NUM_ITEMS: 1,
#     GROC_LIST: {
#         'itemA': '10-20-2022'
#     }
# },
# {
#     USER_NAME: 'user2',
#     LIST_NAME: 'trip2',
#     NUM_ITEMS: 2,
#     GROC_LIST: {
#         'itemB': '11-03-2022',
#         'itemC': '10-30-2022'
#     }
# }


def get_number_of_items(username):
    """
    returns the number of items in a user's grocery list
    """
    for entry in lists:
        if entry[USER_NAME] == username:
            return entry[NUM_ITEMS]
    return None


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
    lists.append(details)


def get_user_groceries(username):
    """
    returns a dictionary of groceries for a user
    """
    for entry in lists:
        if entry[USER_NAME] == username:
            return entry[GROC_LIST]
    return None


def groc_lst_exists(username):
    """
    checks if a grocery list exists for a user
    """
    for groc in lists:
        if groc[USER_NAME] == username:
            return True
    return False


def main():
    usernames = get_usernames()
    print(usernames)


if __name__ == '__main__':
    main()
