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

"""
Ex: {BAKED_GOODS: {'bread': [Quantity you want,
Quanitity you have, Expiration date1,[Notes]]}}
"""
GROC_TYPES = {BAKED_GOODS: {},
              CARBS: {},
              FRUIT: {},
              DAIRY: {},
              VEGETABLES: {},
              SNACKS: {},
              DRINKS: {},
              MEAT: {}}


def get_grocery_types():
    return list(GROC_TYPES.keys())
