"""
This module is for a singular grocery list structure. It contains functions
necessary to interact with a grocery list.
"""

import db.db_connect as dbc

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

GROC_TYPE = 'grocery_type'
QUANTITY = 'quantity'
EXPIRATION_DATE = 'expiration_date'
GROC_COLLECT = "grocdb"
GROC_KEY = "item"

REQUIRED_FIELDS = [GROC_TYPE, QUANTITY, EXPIRATION_DATE]
# example of a grocery list structure
grocery_list = {
    "item1": {
        GROC_TYPE: BAKED_GOODS,
        QUANTITY: 10,
        EXPIRATION_DATE: "10-20-2022"
    }
}


GROC_TYPES = {BAKED_GOODS: {},
              CARBS: {},
              FRUIT: {},
              DAIRY: {},
              VEGETABLES: {},
              SNACKS: {},
              DRINKS: {},
              MEAT: {},
              MISC: {}}


def get_groc_types():
    return list(GROC_TYPES.keys())


def get_groc_types_dict():
    return GROC_TYPES


# All items...? Assume only working with 1 list
def get_items() -> list:
    """
    returns a list of all items in the grocery list
    """
    return list(get_grocery_list().keys())


def get_grocery_list() -> dict:
    """
    returns the entire grocery list
    """
    # return grocery_list
    dbc.connect_db()
    return dbc.fetch_all_as_dict(GROC_KEY, GROC_COLLECT)


def exists(item: str) -> bool:
    """
    returns True if item exists in the grocery list
    """
    return item in get_grocery_list()


# TODO: change to use db
def get_details(item: str) -> dict:
    """
    returns a dictionary of details for a singular grocery item
    """
    return grocery_list[item]


# TODO: change to use db
def get_types():
    """
    returns all unique grocery types in the grocery list
    """
    return list(set([item[GROC_TYPE] for item in grocery_list.values()]))


# TODO: change to use db
def add_item(item: str, details: dict):
    """
    adds an item to the grocery list
    """
    if not isinstance(item, str):
        raise TypeError(f'Wrong type for item: {type(item)=}')
    if exists(item):
        raise ValueError(f'Item {item=} already exists in grocery list.')
    if not isinstance(details, dict):
        raise TypeError(f'Wrong type for details: {type(details)=}')
    for field in REQUIRED_FIELDS:
        if field not in details:
            raise KeyError(f'Required {field=} missing from details.')
    if details[GROC_TYPE] not in get_groc_types():
        raise ValueError(f'Invalid {details[GROC_TYPE]=} in details. '
                         + f'Must be one of: {get_groc_types()}')
    if not isinstance(details[QUANTITY], int):
        raise TypeError(f'Wrong type for quantity: {type(details[QUANTITY])=}')
    grocery_list[item] = details


# TODO: change to use db
def remove_item(item: str):
    """
    removes an item from the grocery list
    """
    if not isinstance(item, str):
        raise TypeError(f'Wrong type for item: {type(item)=}')
    if not exists:
        raise ValueError(f'Item {item=} not in grocery list.')
    del grocery_list[item]


# TODO: change to use db
def update_item(item: str, details: dict):
    """
    Updates all details of an item in the grocery list
    """
    if not isinstance(item, str):
        raise TypeError(f'Wrong type for item: {type(item)=}')
    if not exists(item):
        raise ValueError(f'Item {item=} not in grocery list.')
    if not isinstance(details, dict):
        raise TypeError(f'Wrong type for details: {type(details)=}')
    for field in REQUIRED_FIELDS:
        if field not in details:
            raise KeyError(f'Required {field=} missing from details.')
    if details[GROC_TYPE] not in get_groc_types():
        raise ValueError(f'Invalid {details[GROC_TYPE]=} in details. '
                         + f'Must be one of: {get_groc_types()}')
    if not isinstance(details[QUANTITY], int):
        raise TypeError(f'Wrong type for quantity: {type(details[QUANTITY])=}')
    grocery_list[item] = details


# TODO: change to use db
def update_groc_type(item: str, groc_type: str):
    """
    Updates the grocery type of an item in the grocery list
    """
    if not isinstance(item, str):
        raise TypeError(f'Wrong type for item: {type(item)=}')
    if not exists(item):
        raise ValueError(f'Item {item=} not in grocery list.')
    if not isinstance(groc_type, int):
        raise TypeError(f'Wrong type for quantity: {type(groc_type)=}')
    grocery_list[item][GROC_TYPE] = groc_type


# TODO: change to use db
def update_quantity(item: str, quantity: int):
    """
    Updates the quantity of an item in the grocery list
    """
    if not isinstance(item, str):
        raise TypeError(f'Wrong type for item: {type(item)=}')
    if not exists(item):
        raise ValueError(f'Item {item=} not in grocery list.')
    if not isinstance(quantity, int):
        raise TypeError(f'Wrong type for quantity: {type(quantity)=}')
    grocery_list[item][QUANTITY] = quantity


# TODO: change to use db
def update_expiration(item: str, exp: str):
    """
    Updates expiration date of an item in grocery list
    """
    if not isinstance(item, str):
        raise TypeError(f'Wrong type for item: {type(item)=}')
    if not exists(item):
        raise ValueError(f'Item {item=} not in grocery list.')
    if not isinstance(exp, str):
        raise TypeError(f'Wrong type for expiration date: {type(exp)=}')
    grocery_list[item][EXPIRATION_DATE] = exp


# TODO: change to use db
def get_grocs_by_type(type):
    """
    Returns dictionary containing items of given type
    """
    for key, val in grocery_list.items():
        ret = {}
        if val[GROC_TYPE] == type:
            ret[key] = val
    return val


def del_groc(name):
    return dbc.del_one(GROC_COLLECT, {GROC_KEY: name})


def main():
    # print(get_items())
    # print(get_details("item1"))
    # print(get_types())
    pass


if __name__ == '__main__':
    main()
