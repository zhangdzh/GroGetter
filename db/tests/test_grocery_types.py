"""
module for testing the grocery types
"""

import db.groc_types as gtyp


def test_get_groc_types():
    """
    test get_groc_types
    """
    assert len(gtyp.get_groc_types()) > 0
    assert isinstance(gtyp.get_groc_types(), list)


def test_get_groc_items_by_type():
    """
    test get_groc_items_by_type
    """
    assert isinstance(gtyp.get_groc_items_by_type('Meat'), dict)
