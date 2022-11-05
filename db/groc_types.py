"""
Module encapsulating details of grocery types.
"""

BAKED_GOODS = 'Baked Goods'
CARBS = 'Carbs'
FRUIT = 'Fruit'
DAIRY = 'Dairy'
VEGETABLES = 'Vegetables'
SNACKS = 'Snacks'
DRINKS = 'Drinks'
MEAT = 'Meat'
MISC = 'Misc'

"""
Ex: {BAKED_GOODS: {'bread': [Quantity you want,
Quanitity you have, Expiration date1, [Notes]]}}
Design note: Index 3 in value list is designated
as notes list. Will provide user ability to append
string notes to the list, for freedom of use.
"""
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


def main():
    print(f'Grocery types: {get_groc_types()}')


if __name__ == "__main__":
    main()
