'''
This module encapsulates details about a user's grocery list
'''

USER_NAME = 'name'
LIST_NAME = 'list_name'
NUM_ITEMS = 'num_items'
GROC_LISTS = {}

REQUIRED_FIELDS = [USER_NAME, LIST_NAME, NUM_ITEMS, GROC_LISTS]
lists = {USER_NAME: {LIST_NAME: 'trip1',
                            NUM_ITEMS: 1,
                            GROC_LISTS: {'itemA': '10-20-2022'}},
                'user2': {LIST_NAME: 'trip2',
                          NUM_ITEMS: 2,
                          GROC_LISTS: {'itemB': '11-03-2022',
                                       'itemC': '10-30-2022'}}}


def get_usernames():
    return list(lists.keys())


def main():
    usernames = get_usernames()
    print(usernames)


if __name__ == '__main__':
    main()
