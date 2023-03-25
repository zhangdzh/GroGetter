"""
module for testing the grocery types
"""

import db.deprecated.groc_types as gtyp


def test_get_groc_types():
    """
    test get_groc_types
    """
    assert len(gtyp.get_groc_types()) > 0
    assert isinstance(gtyp.get_groc_types(), list)


def test_get_groc_types_dict():
    """
    test get_groc_types_dict
    """
    assert len(gtyp.get_groc_types_dict()) > 0
    assert isinstance(gtyp.get_groc_types_dict(), dict)
