"""
This module is for a singular grocery list structure. It contains functions
necessary to interact with a grocery list.
"""

import db.db_connect as dbc
from db.users import USERNAME

# Grocery types
BAKED_GOODS = 'Baked Goods'
CARBS = 'Carbs'
FRUIT = 'Fruit'
DAIRY = 'Dairy'
VEGETABLES = 'Vegetables'
SNACKS = 'Snacks'
DRINKS = 'Drinks'
MEAT = 'Meat'
MISC = 'Misc'

groc_types = (BAKED_GOODS, CARBS, FRUIT, DAIRY,
              VEGETABLES, SNACKS, DRINKS, MEAT, MISC)

GROC_TYPE = 'grocery_type'
QUANTITY = 'quantity'
EXPIRATION_DATE = 'expiration_date'
GROC_COLLECT = "grocdb"
ITEM = 'item'

# testing for the manually created grocery list
GROC_KEY = "item1"

REQUIRED_FIELDS = [USERNAME, GROC_TYPE, QUANTITY, EXPIRATION_DATE]

# document structure for mongodb
'''
{
    username: "user1",
    item: "item1",
    grocery_type: BAKED_GOODS,
    quantity: 10,
    expiration_date: "10-20-2022"
}
'''


def get_all_items() -> list:
    """
    Gets all items of all users in the collection

    :return: list of all items
    """
    dbc.connect_db()
    return dbc.fetch_all(GROC_COLLECT)


def get_user_list(user) -> list:
    """
    Gets a user's list of items

    :param user: username of the user
    :return: list of items
    """
    dbc.connect_db()
    filter = {USERNAME: user}
    return dbc.fetch_all_filtered(GROC_COLLECT, filter)


def exists(item: str, user) -> bool:
    """
    Determine if an item exists in the user's grocery list

    :param item: item to check
    :param user: username of the user
    :return: True if item exists, False otherwise
    """
    for doc in get_user_list(user):
        if doc[ITEM] == item:
            return True
    return False


def get_details(item: str, user: str) -> dict:
    """
    Gets the details for a singular grocery item

    :param item: item to get details for
    :param user: username of the user
    :return: dictionary of details
    """
    filter = {ITEM: item, USERNAME: user}
    dbc.connect_db()
    if not exists(item, user):
        raise KeyError(f'Item {item=} not in user\'s list.')
    return dbc.fetch_one(GROC_COLLECT, filter)


def get_types(user) -> list:
    """
    Gets all unique grocery types in the grocery list

    :param user: username of the user
    :return: list of grocery types
    """
    types = []
    for item in get_user_list(user):
        if item[GROC_TYPE] not in types:
            types.append(item[GROC_TYPE])
    return types


def add_item(details: dict):
    """
    Adds an item to the user's grocery list

    :param details: dictionary of details for the item
    """
    if not isinstance(details, dict):
        raise TypeError(f'Wrong type for details: {type(details)=}')
    for field in REQUIRED_FIELDS:
        if field not in details:
            raise KeyError(f'Required {field=} missing from details.')
    dbc.connect_db()
    dbc.insert_one(GROC_COLLECT, details, dbc.GROC_DB)


def remove_item(item: str, user: str):
    """
    Removes an item from the user's grocery list

    :param item: item to remove
    :param user: username of the user
    """
    if not isinstance(item, str):
        raise TypeError(f'Wrong type for item: {type(item)=}')
    if not exists(item, user):
        raise KeyError(f'Item {item=} not in grocery list.')
    dbc.connect_db()
    filt = {ITEM: item, USERNAME: user}
    dbc.del_one(GROC_COLLECT, filt)


def update_item(item: str, user: str, details: dict):
    """
    Updates all details of an item in the grocery list

    :param item: Name of item to update
    :param details: Details to be changed
    """
    if not isinstance(item, str):
        raise TypeError(f'Wrong type for item: {type(item)=}')
    if not exists(item, user):
        raise ValueError(f"Item {item=} not in user's list.")
    if not isinstance(details, dict):
        raise TypeError(f'Wrong type for details: {type(details)=}')
    for field in REQUIRED_FIELDS:
        if field not in details:
            raise KeyError(f'Required {field=} missing from details.')
    if details[GROC_TYPE] not in groc_types:
        raise ValueError(f'Invalid {details[GROC_TYPE]=} in details. '
                         + f'Must be one of: {groc_types}')
    if not isinstance(details[QUANTITY], int):
        raise TypeError(f'Wrong type for quantity: {type(details[QUANTITY])=}')
    # update
    filter = {ITEM: item, USERNAME: user}
    dbc.connect_db()
    dbc.update_one(GROC_COLLECT, filter, details)


def purge():
    """
    Deletes all items from collection
    """
    dbc.connect_db()
    dbc.delete_many(GROC_COLLECT, {})


def main():
    # print(get_items())
    # print(get_details("item1"))
    # print(get_types())
    pass


if __name__ == '__main__':
    main()
