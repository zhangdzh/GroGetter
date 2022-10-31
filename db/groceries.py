"""
This module is for a singular grocery list structure. It contains functions
necessary to interact with a grocery list.
"""

# import groc_types as gtyp

GROC_TYPE = 'grocery_type'
Quantity = 'quantity'
EXPIRATION_DATE = 'expiration_date'

REQUIRED_FIELDS = [GROC_TYPE, Quantity, EXPIRATION_DATE]
# example of a grocery list structure
grocery_list = {
    "item1": {
        GROC_TYPE: None,
        Quantity: "10",
        EXPIRATION_DATE: "10-20-2022"
    }
}


def get_grocery_items():
    """
    returns a list of all items in the grocery list
    """
    return list(grocery_list.keys())


def main():
    print(get_grocery_items())


if __name__ == '__main__':
    main()
